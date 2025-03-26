#!/usr/bin/zsh

filepath_common=/home/chris/showtimes
$filepath_common/showtimes.py
if [ "$?" -eq 1 ]
    then echo "$(date): Emailing updated showtimes..." >> $filepath_common/showtimes.log
    text="$(cat $filepath_common/showtimes.txt)"
    html="$(cat $filepath_common/showtimes.html)"
    subj='Dahlgren Theater - Showtimes'
    for rx in $(awk '{ print $1 }' "$filepath_common/mailing-list.txt")
        do
        /home/chris/.local/bin/send-msg.py --subj "$subj" --rx "$rx" --text "$text" --html "$html"
    done
fi

