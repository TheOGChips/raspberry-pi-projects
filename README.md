# raspberry-pi-projects

Personal projects involving the Raspberry Pi. All projects in this repo will use setup automation via Ansible. Some helpful links used while using Ansible have been linked below.

## Movie Theater Showtime Notification Service

This project is a service that runs on a Raspberry Pi to retrieve movie theater showtimes from a website and email it to a mailing list of recipients. This is intended for smaller local theaters who might not have another method of sending push notifications (e.g. a local theater that is not part of a major chain and therefore might not have something like a mobile app to perform the same function).

### Inspiration

In the author's case, the author kept forgetting to check his local theater's website on a regular basis and worried that he would inevitably miss a film he was interested in seeing, so this service provided a method of updating him in a consistent way since he regularly checks his email.

### E-mail Updates

For the current settings in this project, the service scrapes the website once a day at noon local time and emails are sent out only when the theater's website updates the list of showtimes. Even though this repo refers to this project as a "service", this is actually not run as a `systemd` service but rather as a `cron` job. While this project was designed with a movie theater website in mind, this can be adapted to use any website that similarly updates a table of information on a regular basis. Most modern email clients should be able to display the HTML table that this service sends, but if a recipient's email client is incapable of this, nicely formatted text output that will appear similar to the HTML table will be displayed instead.

### E-mail List

The mailing list is a text file (`mailing-list.txt`) where the first column of each line must be an email that will receive the update. Additional columns are ignored by the parser, which allows populating with helpful information such as the person's name that owns the email. In the interest of privacy, the service actually sends out one email per subscriber in the mailing list rather than accumulating all subscribers into into the recipients list of one email. This project does not provide a way of adding or removing users via the command line, nor does the author intend to add such functionality, so this must be done manually.

### E-mail Server Settings

This project uses Python's `email` module from its standard library to send out emails. This project assumes that the user has set up a password that external applications (e.g. this notification service) can use to authenticate with the user's email provider (e.g. Google, Yahoo!, Apple, Proton, etc.) in order to send emails. For security reasons, these authentication credentials have been stored in a file called `secrets.py` and referenced by the main Python script and the Ansible playbook, and the author's personal `secrets.py` file has been ignored by this repo. As such, the user of this service will need to create their own `secrets.py` with the following string variables:

- `EMAIL`: The email used to send email updates to the subscribers in the mailing list.
- `PASSWORD`: The password used by an external service to authenticate with the provider of `EMAIL`. This should NOT be your regular email login password. The following links should help you with creating one:
    - [Sending Email with iCloud in Python](https://stackoverflow.com/questions/57060199/sending-email-with-icloud-in-python)
    - [Sending an email with Python from a Protonmail account, SMTP library](https://stackoverflow.com/questions/56330521/sending-an-email-with-python-from-a-protonmail-account-smtp-library)
- `URL`: The URL for the website to scrape.

### Text Messages

The Python script that performs the email function, `send-msg.py`, is also capable of being used to send text messages; however, in the author's experience, this was less reliable than traditional emails, and text messages don't allow the display of nicely formatted HTML tables as emails do. Regardless, if you decide to try the text message method instead, this link should be able to help: [How to send text messages with Python for Free](https://medium.com/testingonprod/how-to-send-text-messages-with-python-for-free-a7c92816e1a4)

### Command Line Interface

If the Python script is run directly, the text formatted output will be displayed in the terminal output instead of being emailed to the mailing list. Using this functionality should not affect when the service will send out emails and can be done by running:

    `python showtimes.py --print`

## Hardware

The exact model of Raspberry Pi will be listed below, although this code should be compatible with any computer that has Internet connection capability, not just Raspberry Pis.

- [Raspberry Pi Zero Wireless WH (Pre-Soldered Header)](https://www.pishop.us/product/raspberry-pi-zero-wireless-wh-pre-soldered-header/)
- [Official Raspberry Pi Zero Case + Mini Camera Cable](https://www.pishop.us/product/official-raspberry-pi-zero-case-mini-camera-cable/)
- [iUniker micro-USB Power Supply with Toggle Switch](https://www.amazon.com/Listed-iUniker-Raspberry-Supply-Switch/dp/B0B79FVPQ4/ref=sr_1_1?crid=22UGFI3C0LK9K&dib=eyJ2IjoiMSJ9.YJuNRqAe773WQMisM57WNIWv_Crh-kNpQ211kaUzDVozeD6xHYJiPQCdn6IpUDUmWke8DPmKKlQ-xNSVg2XbD7rUGS2ulJ0EIjkYXXGWCohvdmedrDay-kdeQ_h0SRezeD58O-ZZYelgDebEipOtOUvkJP3bEPz8N8Jo0Hmh6luiQHzCdzMIiPClVsehnfT545YfmDPyp3e3282MBr0vnukxxtjSgT7L2zMAmprdvK2uHxAu9nXhqlYTdr3leWE55RN9wNRf1w_rcyRlLUi4Wbt2czaSx7ROZMtd00SSBWcTa2r25m7ONnA2b_kp4EtnxXuBn06xcDsrf7FmvJKmswZN_wdeftRG9HcTYMbbqVY.M_hYLdPsAsyANbkIekQbgl8dlban9rJZVsZWjfm5yQo&dib_tag=se&keywords=%5B5V+3A+UL+Listed%5D+iUniker+Power+Supply+for+Raspberry+Pi+3%2C+Power+Supply+for+Raspberry+Pi+MicroUSB+Power+Supply+with+on%2Foff+Switch+Compatible+with+Raspberry+Pi+3%2F+3b%2B%2F+Zero%2FZero+2w&qid=1742705952&s=electronics&sprefix=5v+3a+ul+listed+iuniker+power+supply+for+raspberry+pi+3%2C+power+supply+for+raspberry+pi+microusb+power+supply+with+on%2Foff+switch+compatible+with+raspberry+pi+3%2F+3b%2B%2F+zero%2Fzero+2w+%2Celectronics%2C142&sr=1-1)
- [MicroSD Card - 32 GB - Class 10 - BLANK](https://www.pishop.us/product/microsd-card-32-gb-class-10-blank/)

## Prerequisites

This project assumes you know how to:

- Image a microSD card with Raspberry Pi OS
    - I recommend using the Raspberry Pi Imager tool
    - Setting the hostname to `raspberrypi.local` will let you avoid changing the entry in `hosts.txt`
    - Setting the Raspberry Pi username to the same as your username on your computer will let you avoid having to change the `remote_user` field in `main.yml`
- Enable and remotely access a Raspberry Pi over SSH
- Generate an SSH key and transfer the public key over to the Raspberry Pi

There are plenty of tutorials online about how to do each of these things.

## Installation

1. Make sure you can remotely access your Raspberry Pi over SSH. Note that if you bought a Raspberry Pi Zero (the one without Wi-Fi accessibilty) you will need to also buy an adapter of some sort, likely a micro-USB-to-Ethernet adapter.

1. Ensure that your Raspberry Pi can access the Internet.

1. Set up an SSH key for the Raspberry Pi on your computer and transfer the public key over to the Raspberry Pi.

1. Change the filepath to the SSH key in `ansible.cfg` for the entry `private_key_file`.

1. Change the hostname of the Raspberry Pi in `hosts.txt` if you opted to use something different. You should be able to use the `.local`-styled hostname instead of the actual IP address.

1. In `main.yml`, the field `remote_user` currently assumes you set the Raspberry Pi's username to the same username on your computer. If you did not do this, edit this field to match the username on the Raspberry Pi.

1. Run the Ansible playbook for setting up the Raspberry Pi.

    `ansible-playbook -K main.yml`

1. If you didn't change the `cron` settings from the "Updating Raspberry Pi crontab" step of `main.yml`, the service will run the next time the Raspberry Pi's clock reaches 12:00 p.m.; otherwise, it will run at the time you changed the settings to. Note that an email notification should be sent the very first time the service is run, and subsequent emails will only be sent when the service determines there has been an update. If the service attempts to send emails but none are received within a few minutes of the scheduled time there are two possiblities why:

    - An error likely occurred during install, and you will need to troubleshoot why.
    - Your email has for some reason been marked as undeliverable by your service provider. You should receive an email indicating this at `EMAIL` within about 24 hours or so. Unfortunately, the isn't a way known to the auther to fix this aside from attempting to keep this from happening. Removing the autogenerated files and manually running via `bash showtimes.sh` will force another email update to be sent and "correct" this issue. This also won't affect future attempts to send emails, so you can also choose to just ignore this error and wait until the next time the service attempts to send emails.

## Helpful Sources

- [Use Ansible to automate installation and deployment of Raspberry boxes](https://robertopozzi.medium.com/use-ansible-to-automate-installation-and-deployment-of-raspberry-boxes-cfe04ac10ce6)
- [Specify sudo password for Ansible](https://medium.com/@haroldfinch01/specify-sudo-password-for-ansible-1150e8bb19d7)
