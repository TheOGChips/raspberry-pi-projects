#!/usr/bin/python3

# src: https://medium.com/testingonprod/how-to-send-text-messages-with-python-for-free-a7c92816e1a4
# src: https://stackoverflow.com/questions/57060199/sending-email-with-icloud-in-python

# WARNING: If using a Proton email, this must be sent from a machine where ProtonMail Bridge is actively running.
# WARNING: If sending to another Proton email, the use of MIME might be needed
# src: https://stackoverflow.com/questions/56330521/sending-an-email-with-python-from-a-protonmail-account-smtp-library

# NOTE: I've also noticed that there appears to be a 30-minute refresh period that's required if trying to send 
#		exactly the same message repeatedly. I'm not quite sure why this is now an problem. The simplest 
#		workaround seems to be sending a slightly different message if testing rapidly, which can either be a 
#		change in either the message contents or the subject line by at least one character. The smartest way to 
#		do this would be adding the current date and time via the 'date' command.

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from sys import argv, exit
import re
import secrets

EMAIL = secrets.EMAIL
PASSWORD = secrets.PASSWORD
MY_PHONE_NO = secrets.MY_PHONE_NO

# NOTE: Both carrier domains for Ting Mobile appear to work with my
#       phone for some reason
CARRIERS = {
    'att': '@txt.att.net',
    'tmobile': '@tmomail.net',
    'verizon': '@vtext.com',
    'sprint': '@messaging.sprintpcs.com',
    #'ting': '@message.ting.com' # for CDMA
    'ting': '@tmomail.net'      # for GSM
}

def parse_clargs ():
    args = argv[1:]

    # NOTE: Set default values before parsing
    rx = MY_PHONE_NO
    cx = CARRIERS['ting']
    subj = 'Python Notification System'
    plaintext = '(blank message)'
    html = plaintext

    # NOTE: Now parse command line arguments
    options = ['--rx', '--carrier', '--subj', '--text', '--html']
    while (len(args) > 0):
        # if (args[0] != '--rx' and args[0] != '--carrier' and args[0] != '--subj'):
        #     msg = args[0]
        #     args = args[1:]
        if not options.count(args[0]):
            msg = args[0]
            html = args[0]
            args = args[1:]
        else:
            try:
                if (args[0] == '--rx'):
                    if re.search('@(passmail.net|google.com|icloud.com)', args[1]):
                        rx = args[1]
                        cx = ''
                    else:
                        rx = str(int(args[1]))
                        if len(rx) != 10: raise ValueError
                elif (args[0] == '--carrier') and cx != '':
                    cx = CARRIERS[args[1]]
                elif (args[0] == '--subj'):
                    subj = args[1]
                elif args[0] == '--text':
                    plaintext = args[1]
                    # html = args[1] if html == '(blank message)' else html
                elif args[0] == '--html':
                    html = args[1]
                    # plaintext = args[1] if plaintext == '(blank message)' else plaintext

                args = args[2:]
            except (ValueError, KeyError) as err:
                if type(err) is ValueError:
                    print('Error with arg', args[1])
                    print('rx must be a valid 10-digit cell phone number with no dashes')
                elif type(err) is KeyError:
                    print('Error with arg', args[1])
                    print('carrier options -> att, tmobile, verizon, sprint, or ting')
                exit(1)

    return rx, cx, subj, plaintext, html

def send_msg (phone_no: str, carrier: str, subj: str, text: str, html: str):
    rx = phone_no + carrier
    #print(rx, ':', msg)
    #sys.exit(1)

	# NOTE: Look up this SMTP IP and port # on ProtonMail Bridge
    server = smtplib.SMTP('smtp.mail.me.com', 587)
    server.ehlo()
    server.starttls()
    server.login(EMAIL, PASSWORD)
    while True:
        try:
            msg = MIMEMultipart(_subtype='alternative')
            attachments = []
            if text == html == '(blank message)':
                attachments.append(MIMEText(text))
            elif text == '(blank message)':
                attachments.append(MIMEText(html, _subtype='html'))
            elif html == '(blank message)':
                attachments.append(MIMEText(text))
            else:
                attachments.append(MIMEText(text))
                attachments.append(MIMEText(html, _subtype='html'))
            # NOTE: Attaching plaintext and html versions. The email browser on the receiver's end will
            for attachment in attachments:
                msg.attach(attachment)
            msg['From'] = EMAIL
            msg['To'] = rx
            msg['Subject'] = subj
            server.sendmail(EMAIL, rx, msg.as_string())
            break
        except smtplib.SMTPDataError as err:
            print(err)
            continue
    server.quit()

if __name__ == '__main__':
    #print(len(argv))
    if len(argv) > 11 or '--help' in argv:
        print('''
Error: Too many arguments!

Usage: send-msg.py [options] <msg>

Options:
       --rx <rx> -> <rx> phone number with no dashes
                    <rx> email address
       --carrier <carrier> -> <carrier> is one of the following:
                              att, tmobile, verizon, sprint, or ting
       --subj <subj> -> <subj> is the subject line enclosed in quotes
       --text <text> -> <text> is plaintext part enclosed in quotes
       --html <html> -> <html> is html part enclosed in quotes
''')
        exit(1)
    else:
        # https://stackoverflow.com/questions/691267/passing-functions-which-have-multiple-return-values-as-arguments-in-python
        # NOTE: The star operator here unpacks the return arguments from
        #       parse_clargs. Source is at the StackOverflow link on the line
        #       above.
        send_msg(*parse_clargs())
