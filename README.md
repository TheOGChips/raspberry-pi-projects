# raspberry-pi-projects

Personal projects involving the Raspberry Pi. All projects in this repo will use setup automation via Ansible. Some helpful links used while using Ansible have been linked below.

## Backup Server

This project configures a Raspberry Pi with an external hard drive used for remote backups. This is useful if you need a regular place to backup your computer over SSH.

## Hardware

The exact model of Raspberry Pi will be listed below, although this code should be compatible with any Linux computer that has Internet connection capability, not just Raspberry Pis.

- [Raspberry Pi Zero Wireless WH (Pre-Soldered Header)](https://www.pishop.us/product/raspberry-pi-zero-wireless-wh-pre-soldered-header/)
- [Official Raspberry Pi Zero Case + Mini Camera Cable](https://www.pishop.us/product/official-raspberry-pi-zero-case-mini-camera-cable/)
- [iUniker micro-USB Power Supply with Toggle Switch](https://www.amazon.com/Listed-iUniker-Raspberry-Supply-Switch/dp/B0B79FVPQ4/ref=sr_1_1?crid=22UGFI3C0LK9K&dib=eyJ2IjoiMSJ9.YJuNRqAe773WQMisM57WNIWv_Crh-kNpQ211kaUzDVozeD6xHYJiPQCdn6IpUDUmWke8DPmKKlQ-xNSVg2XbD7rUGS2ulJ0EIjkYXXGWCohvdmedrDay-kdeQ_h0SRezeD58O-ZZYelgDebEipOtOUvkJP3bEPz8N8Jo0Hmh6luiQHzCdzMIiPClVsehnfT545YfmDPyp3e3282MBr0vnukxxtjSgT7L2zMAmprdvK2uHxAu9nXhqlYTdr3leWE55RN9wNRf1w_rcyRlLUi4Wbt2czaSx7ROZMtd00SSBWcTa2r25m7ONnA2b_kp4EtnxXuBn06xcDsrf7FmvJKmswZN_wdeftRG9HcTYMbbqVY.M_hYLdPsAsyANbkIekQbgl8dlban9rJZVsZWjfm5yQo&dib_tag=se&keywords=%5B5V+3A+UL+Listed%5D+iUniker+Power+Supply+for+Raspberry+Pi+3%2C+Power+Supply+for+Raspberry+Pi+MicroUSB+Power+Supply+with+on%2Foff+Switch+Compatible+with+Raspberry+Pi+3%2F+3b%2B%2F+Zero%2FZero+2w&qid=1742705952&s=electronics&sprefix=5v+3a+ul+listed+iuniker+power+supply+for+raspberry+pi+3%2C+power+supply+for+raspberry+pi+microusb+power+supply+with+on%2Foff+switch+compatible+with+raspberry+pi+3%2F+3b%2B%2F+zero%2Fzero+2w+%2Celectronics%2C142&sr=1-1)
- [MicroSD Card - 32 GB - Class 10 - BLANK](https://www.pishop.us/product/microsd-card-32-gb-class-10-blank/)
- [Toshiba Canvio Flex 1TB Portable External Hard Drive USB-C USB 3.0, Silver for PC, Mac, & Tablet - HDTX110XSCAA](https://www.amazon.com/Toshiba-Canvio-Portable-External-Silver/dp/B08JKH2DS2/ref=sr_1_5?crid=24EM5LRD5VXKG&dib=eyJ2IjoiMSJ9.tmKpjww6SZR6ksgJLlgQ4GmByZ-aj76jN6MmcFb3KDl2Gw3xGT70ahOER-ruhy0yZG3sBI0a-upGG22IHFqH13eWQOjMLtBKvv7x0bHbkVJPsJGXBUp6IuEnff6F0m9A0pnPYFtOcXGCTUjBYA0sLUH_ZQgo4Rl68OvFFahLV9tTRUwuLGVyE1fUoWS514SESYFOUgNCVpelkZXqhPNzn014kjSx4EWCk50TRJMONfc.s1XD3jvXk0PNAjW1XMsERtlw1BjYR0EbUHG045kBtrA&dib_tag=se&keywords=toshiba%2B1tb%2Bexternal%2Bhard%2Bdrive&qid=1743359202&sprefix=toshiba%2B1%2Caps%2C133&sr=8-5&th=1)

## Prerequisites

This project assumes you know how to:

- Image a microSD card with Raspberry Pi OS
    - I recommend using the Raspberry Pi Imager tool
    - Setting the hostname to `raspberrypi.local` will let you avoid changing the entry in `hosts.txt`
    - Setting the Raspberry Pi username to the same as your username on your computer will let you avoid having to change the `remote_user` field in `main.yml`
- Enable and remotely access a Raspberry Pi over SSH
- Generate an SSH key and transfer the public key over to the Raspberry Pi

There are plenty of tutorials online about how to do each of these things.

For the different `fstab` options, see [fstab(5)](https://man7.org/linux/man-pages/man5/fstab.5.html).

## Installation

1. Make sure you can remotely access your Raspberry Pi over SSH. Note that if you bought a Raspberry Pi Zero (the one without Wi-Fi accessibilty) you will need to also buy an adapter of some sort, likely a micro-USB-to-Ethernet adapter.

1. Ensure that your Raspberry Pi can access the Internet.

1. Set up an SSH key for the Raspberry Pi on your computer and transfer the public key over to the Raspberry Pi.

1. Change the filepath to the SSH key in `ansible.cfg` for the entry `private_key_file`.

1. Change the hostname of the Raspberry Pi in `hosts.txt` if you opted to use something different. You should be able to use the `.local`-styled hostname instead of the actual IP address.

1. In `main.yml`, the field `remote_user` currently assumes you set the Raspberry Pi's username to the same username on your computer. If you did not do this, edit this field to match the username on the Raspberry Pi.

1. Run the Ansible playbook for setting up the Raspberry Pi.

    `ansible-playbook -K main.yml`

1. Reboot the Raspberry Pi and verify that you can access the backup hard drive.

## Helpful Sources

- [Use Ansible to automate installation and deployment of Raspberry boxes](https://robertopozzi.medium.com/use-ansible-to-automate-installation-and-deployment-of-raspberry-boxes-cfe04ac10ce6)
- [Specify sudo password for Ansible](https://medium.com/@haroldfinch01/specify-sudo-password-for-ansible-1150e8bb19d7)
