#!/home/chris/showtimes/.showtimes-venv/bin/python

import requests
import pandas as pd
from datetime import datetime
import sys
import os
import enum
import subprocess
import secrets

def to_plaintext (showtimes_list: list) -> str:
    display_str = '\n\n'
    for day in showtimes_list:
        cols = [col for col in day.columns]
        cols.remove(cols[2])    # Remove the movie rating (shows as NaN)

        showtimes = [showtime for showtime in day[cols[0]]]
        titles = [title for title in day[cols[1]]]
        runtimes = [runtime for runtime in day[cols[2]]]
        assert len(showtimes) == len(titles) == len(runtimes)

        buffer = 2
        max_time_len = max([len(showtime) for showtime in showtimes]) + buffer
        max_movie_title_len = max([len(title) for title in titles]) + buffer
        day = cols[0]
        fmt_str = '%-' + str(max_time_len) + 's %-' + str(max_movie_title_len) + 's %-10s'

        display_str += day + '\n'

        # if len(sys.argv) == 2 and sys.argv[1] == '--text-msg':
        #     showtime_header = showtimes[0]
        #     title_header = titles[0]
        #     runtime_header = runtimes[0]
        #     for showtime, title, runtime in zip(showtimes[1:], titles[1:], runtimes[1:]):
        #         display_str += '%s:       %s' %(showtime_header, showtime) + '\n'
        #         display_str += '%s:       %s' %(title_header, title) + '\n'
        #         display_str += '%s:       %s' %(runtime_header, runtime) + '\n'
        # else:
        for showtime, title, runtime in zip(showtimes, titles, runtimes):
            display_str += fmt_str %(showtime, title, runtime) + '\n'

        display_str += '\n\n'

    return display_str

def to_html (showtimes_list: list) -> str:
    showtimes = []
    for day in showtimes_list:
        cols = [col for col in day.columns]
        day.drop(cols[2], axis=1, inplace=True)
        cols.remove(cols[2])

        showtimes_list = [showtime for showtime in day[cols[0]]]
        titles = [title for title in day[cols[1]]]
        runtimes = [runtime for runtime in day[cols[2]]]
        assert len(showtimes_list) == len(titles) == len(runtimes)

        day = {}
        day[showtimes_list[0]] = showtimes_list[1:]
        day[titles[0]] = titles[1:]
        day[runtimes[0]] = runtimes[1:]
        showtimes.append((cols[0], pd.DataFrame(day)))

    html = '''
<html>
  <style> th, td { padding: 5px; } th { text-align: left; } </style>
  <h1> Dahlgren Theater Showtimes </h1>
'''
    for day in showtimes:
        html += f'<h2>{day[0]}</h2>'
        html += f'<body>{day[1].to_html(index=False)}</body>'
    html += '''
</html>
'''
    return html

def get_showtimes (to_stdout: bool):
    filepath = lambda filename: os.path.join('/home/chris/showtimes', filename)
    class ExitCode (enum.Enum):
        DoNotNotify = 0
        Notify = 1
        ErrorWebpageGet = 2

    try:
        # NOTE: Get the latest update from the MWR's website
        url = secrets.URL
        web_page = requests.get(url)
        table_get = pd.read_html(web_page.content)

        if to_stdout:
            print(to_plaintext(table_get))
            return
        else:
            with open(filepath('showtimes.txt'), 'w') as outfile:
                outfile.write(to_plaintext(table_get))

        # NOTE: Get the saved showtimes from the previous day
        table_saved = pd.read_html(open(filepath('showtimes-raw.html')))

        # NOTE: The any call here reduces the N x N matrix down to an N-element list where True means that day's
        #       showtimes are present in the new table and the saved table, and this is not a reason to notify
        #       that there are updated showtimes. The all call reduces this down to a single boolean, so if a
        #       day's showtimes from the newly gotten table aren't found in the saved table, then that measn a
        #       notification needs to be sent out.
        # NOTE: Check if there's been an update on the website that you need to notify the subscribers about
        notify = not all([any([day1.equals(day2) for day2 in table_saved]) for day1 in table_get])
    except FileNotFoundError:
        msg404 = "ERROR 404: This must be the first time you've run this script"
        print(f'{msg404}')
        timestamp = subprocess.run('date', stdout=subprocess.PIPE, text=True).stdout.strip()
        with open(filepath('showtimes.log'), 'w+') as outfile:
            outfile.write(f'{timestamp}: {msg404}\n')
        notify = True
    except Exception as exc:
        timestamp = subprocess.run('date', stdout=subprocess.PIPE, text=True).stdout.strip()
        with open(filepath('showtimes.log'), 'w+') as outfile:
            
            outfile.write(f'''
{timestamp}: {exc}
{timestamp}: Error getting theater site content. Check that the URL is valid.
''')
        sys.exit(ExitCode.ErrorWebpageGet.value)

    if notify:
        with open(filepath('showtimes-raw.html'), 'w') as outfile:
            for day in table_get:
                outfile.write(day.to_html(index=False))
        with open(filepath('showtimes.html'), 'w') as outfile:
            outfile.write(to_html(table_get))
        sys.exit(ExitCode.Notify.value)
    else:
        sys.exit(ExitCode.DoNotNotify.value)

if __name__ == '__main__':
    get_showtimes(sys.argv.count('--print'))

