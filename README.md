# raspberry-pi-projects

Personal projects involving the Raspberry Pi. All projects in this repo will use setup automation via Ansible. Some helpful links used while using Ansible have been linked below.

## Pumpkin Pi

This project contains a Python driver and startup service scripts for a Halloween-themed pumpkin-shaped LED PCB attached to a Raspberry Pi. Once installed via Ansible, the pumpkin PCB should begin its light up pattern once the Raspberry Pi finishes starting up and should run until the Raspberry Pi is manually powered off. The pumpkin PCB used in this project attaches to a Raspberry Pi via an adapter to the Raspberry Pi's 40-pin header. The exact model of Raspberry Pi will be listed in the *Hardware* section, although this code should be compatible with any model of Raspberry Pi since the Python code doesn't require an Internet connection.

## Hardware

- [Raspberry Pi Zero Wireless WH (Pre-Soldered Header)](https://www.pishop.us/product/raspberry-pi-zero-wireless-wh-pre-soldered-header/)
- [Raspberry Pi Halloween Pumpkin Programmable Kit](https://www.pishop.us/product/raspberry-pi-halloween-pumpkin-programmable-kit/)
- [GPIO Stacking Header for Pi – Extra-long 2×20 Pins](https://www.pishop.us/product/gpio-stacking-header-for-pi-extra-long-2-20-pins/)
- [Official Raspberry Pi Zero Case + Mini Camera Cable](https://www.pishop.us/product/official-raspberry-pi-zero-case-mini-camera-cable/)
- [iUniker micro-USB Power Supply with Toggle Switch](https://www.amazon.com/Listed-iUniker-Raspberry-Supply-Switch/dp/B0B79FVPQ4/ref=sr_1_1?crid=22UGFI3C0LK9K&dib=eyJ2IjoiMSJ9.YJuNRqAe773WQMisM57WNIWv_Crh-kNpQ211kaUzDVozeD6xHYJiPQCdn6IpUDUmWke8DPmKKlQ-xNSVg2XbD7rUGS2ulJ0EIjkYXXGWCohvdmedrDay-kdeQ_h0SRezeD58O-ZZYelgDebEipOtOUvkJP3bEPz8N8Jo0Hmh6luiQHzCdzMIiPClVsehnfT545YfmDPyp3e3282MBr0vnukxxtjSgT7L2zMAmprdvK2uHxAu9nXhqlYTdr3leWE55RN9wNRf1w_rcyRlLUi4Wbt2czaSx7ROZMtd00SSBWcTa2r25m7ONnA2b_kp4EtnxXuBn06xcDsrf7FmvJKmswZN_wdeftRG9HcTYMbbqVY.M_hYLdPsAsyANbkIekQbgl8dlban9rJZVsZWjfm5yQo&dib_tag=se&keywords=%5B5V+3A+UL+Listed%5D+iUniker+Power+Supply+for+Raspberry+Pi+3%2C+Power+Supply+for+Raspberry+Pi+MicroUSB+Power+Supply+with+on%2Foff+Switch+Compatible+with+Raspberry+Pi+3%2F+3b%2B%2F+Zero%2FZero+2w&qid=1742705952&s=electronics&sprefix=5v+3a+ul+listed+iuniker+power+supply+for+raspberry+pi+3%2C+power+supply+for+raspberry+pi+microusb+power+supply+with+on%2Foff+switch+compatible+with+raspberry+pi+3%2F+3b%2B%2F+zero%2Fzero+2w+%2Celectronics%2C142&sr=1-1)
- [MicroSD Card - 32 GB - Class 10 - BLANK](https://www.pishop.us/product/microsd-card-32-gb-class-10-blank/)

## Prerequisites

This project assumes you know how to:

- Image a microSD card with Raspberry Pi OS
    - I recommend using the Raspberry Pi Imager tool
    - Setting the hostname to `pumpkin-pi.local` will let you avoid changing the entry in `hosts.txt`
    - Setting the Raspberry Pi username to the same as your username on your computer will let you avoid having to change the `remote_user` field in `main.yml`
- Enable and remotely access a Raspberry Pi over SSH
- Generate an SSH key and transfer the public key over to the Raspberry Pi

There are plenty of tutorials online about how to do each of these things.

## Installation

1. Attach the pumpkin PCB to the Raspberry Pi. The 40-pin adapter on the PCB likely won't be long enough to fit through the opening in the Raspberry Pi case exposing the GPIO pins, so the PCB will need to be attached via the 40-pin extended adapter to the Raspberry Pi's GPIO pins. The PCB should be attached so that the LEDs on the PCB are facing away from the Raspberry Pi.

1. Make sure you can remotely access your Raspberry Pi over SSH. Note that if you bought a Raspberry Pi Zero (the one without Wi-Fi accessibilty) you will need to also buy an adapter of some sort, likely a micro-USB-to-Ethernet adapter.

1. Ensure that your Raspberry Pi can access the Internet. If you bought an older model that cannot do this easily, you will need to do a little more editing to `main.yml` to disable or remove the Ansible tasks that require Internet access, but the Python files that control the pumpkin PCB will still work without Internet access.

1. Set up an SSH key for the Raspberry Pi on your computer and transfer the public key over to the Raspberry Pi.

1. Change the filepath to the SSH key in `ansible.cfg` for the entry `private_key_file`.

1. Change the hostname of the Raspberry Pi in `hosts.txt` if you opted to use something different. You should be able to use the `.local`-styled hostname instead of the actual IP address.

1. In `main.yml`, the field `remote_user` currently assumes you set the Raspberry Pi's username to the same username on your computer. If you did not do this, edit this field to match the username on the Raspberry Pi.

1. Run the Ansible playbook for setting up the Raspberry Pi.

    `ansible-playbook -K main.yml`

1. Once the playbook finishes running, reboot the Raspberry Pi. The pumpkin PCB should start lighting up in a random sequence of different patterns once the Raspberry Pi finishes starting up. This won't happen immediately and can take up to roughly 30 seconds. If longer time than this passes with no activity on the pumpkin PCB, it's possible an error might have occurred and will require further investigation.

## Helpful Sources

- [Use Ansible to automate installation and deployment of Raspberry boxes](https://robertopozzi.medium.com/use-ansible-to-automate-installation-and-deployment-of-raspberry-boxes-cfe04ac10ce6)
- [Specify sudo password for Ansible](https://medium.com/@haroldfinch01/specify-sudo-password-for-ansible-1150e8bb19d7)
