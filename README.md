# raspberry-pi-projects

Personal projects involving the Raspberry Pi. All projects in this repo will use setup automation via Ansible. Some helpful links used while using Ansible have been linked below.

## Webcam

This project sets up a Raspberry Pi to broadcast a live feed from a camera over an IP address, so that it can be seen from any web browser. The original intent for this project was to display color feed during daylight hours and IR feed during low-light and nighttime hours. However, the author experienced difficulties getting the chosen camera to change modes reliably after 24 hours, and resorted to always broadcasting the IR feed instead of rebooting the Raspberry Pi ever 24 hours. However, the now unused files from the original intended functionality have been left in this repository for posterity (or for someone else to fix if they so wish).

## Hardware

The exact model of Raspberry Pi will be listed below, although this code should be compatible with any computer that has Internet connection capability, not just Raspberry Pis.

- [Raspberry Pi Zero 2 W](https://www.pishop.us/product/raspberry-pi-zero-2-w/)
- [Tripod for Raspberry Pi HQ camera](https://www.pishop.us/product/tripod-for-raspberry-pi-hq-camera/)
- [iUniker micro-USB Power Supply with Toggle Switch](https://www.amazon.com/Listed-iUniker-Raspberry-Supply-Switch/dp/B0B79FVPQ4/ref=sr_1_1?crid=22UGFI3C0LK9K&dib=eyJ2IjoiMSJ9.YJuNRqAe773WQMisM57WNIWv_Crh-kNpQ211kaUzDVozeD6xHYJiPQCdn6IpUDUmWke8DPmKKlQ-xNSVg2XbD7rUGS2ulJ0EIjkYXXGWCohvdmedrDay-kdeQ_h0SRezeD58O-ZZYelgDebEipOtOUvkJP3bEPz8N8Jo0Hmh6luiQHzCdzMIiPClVsehnfT545YfmDPyp3e3282MBr0vnukxxtjSgT7L2zMAmprdvK2uHxAu9nXhqlYTdr3leWE55RN9wNRf1w_rcyRlLUi4Wbt2czaSx7ROZMtd00SSBWcTa2r25m7ONnA2b_kp4EtnxXuBn06xcDsrf7FmvJKmswZN_wdeftRG9HcTYMbbqVY.M_hYLdPsAsyANbkIekQbgl8dlban9rJZVsZWjfm5yQo&dib_tag=se&keywords=%5B5V+3A+UL+Listed%5D+iUniker+Power+Supply+for+Raspberry+Pi+3%2C+Power+Supply+for+Raspberry+Pi+MicroUSB+Power+Supply+with+on%2Foff+Switch+Compatible+with+Raspberry+Pi+3%2F+3b%2B%2F+Zero%2FZero+2w&qid=1742705952&s=electronics&sprefix=5v+3a+ul+listed+iuniker+power+supply+for+raspberry+pi+3%2C+power+supply+for+raspberry+pi+microusb+power+supply+with+on%2Foff+switch+compatible+with+raspberry+pi+3%2F+3b%2B%2F+zero%2Fzero+2w+%2Celectronics%2C142&sr=1-1)
- [MicroSD Card - 32 GB - Class 10 - BLANK](https://www.pishop.us/product/microsd-card-32-gb-class-10-blank/)
- [RPi IR-CUT Camera (B)](https://www.waveshare.com/wiki/RPi_IR-CUT_Camera_\(B))
- [Raspberry Pi Zero v1.3 Camera Cable, 150mm](https://www.pishop.us/product/raspberry-pi-zero-v1-3-camera-cable/)
- [Female to Female Jumper Cable x 40 (20cm)](https://www.pishop.us/product/female-to-female-jumper-cable-x-40-20cm/)
- [Break Away Headers - 40-pin Male (Long Centered, PTH, 0.1")](https://www.pishop.us/product/break-away-headers-40-pin-male-long-centered-pth-0-1/)
- [ProtoStax Camera Kit for Waveshare RPi IR-CUT Camera](https://www.protostax.com/products/protostax-camera-kit-for-waveshare-rpi-ir-cut-camera?variant=40801890631846)
- [ProtoStax Enclosure for Raspberry Pi Zero](https://www.protostax.com/products/protostax-for-raspberry-pi-zero)
- [CHICAGO ELECTRIC 30 Watt Lightweight Soldering Iron](https://www.harborfreight.com/30-watt-lightweight-soldering-iron-69060.html)
- [CHICAGO ELECTRIC Lead-Free Rosin Core Solder](https://www.harborfreight.com/lead-free-rosin-core-solder-69378.html)

## Prerequisites

This project assumes you know how to:

- Image a microSD card with Raspberry Pi OS
    - I recommend using the Raspberry Pi Imager tool
    - Setting the hostname to `raspberrypi.local` will let you avoid changing the entry in `hosts.txt`
    - Setting the Raspberry Pi username to the same as your username on your computer will let you avoid having to change the `remote_user` field in `main.yml`
- Enable and remotely access a Raspberry Pi over SSH
- Generate an SSH key and transfer the public key over to the Raspberry Pi
- Solder header pins to a Raspberry Pi header and other circuit boards.
- Open a forwarded port on your Wi-Fi router.

There are plenty of tutorials online about how to do each of these things.

## Installation

### Hardware

1. Solder a header pin to the GPIO pin of the camera circuit board. The location can be seen in the picture at the bottom of [this Q&A question](https://www.waveshare.com/wiki/RPi_IR-CUT_Camera_(B)#accordion3).

1. Solder a header pin to GPIO pin 23 on the Raspberry Pi's header. This will allow toggling between normal/color and IR modes on the camera. Alternatively, you can solder a header pin to a ground (GND) pin to permanently enable IR mode or to one of of the 3.3V (3V3) pins to permanently enable normal/color mode.

1. Attach the camera PCB to the camera to the camera mount top plate of the ProtoStax case. If you don't have an external light source, you can also attach the provided IR lights to the camera board.

1. Mount the Raspberry Pi to the inside of the bottom plate of the ProtoStax case.

    - It will be easier to attach the microSD card before assembling the rest of the case.

1. Attach the ribbon cable from the camera to the appropriate connector on the Raspberry Pi. The connector will be different depending on the model of Raspberry Pi.

1. Attach a female-to-female jumper wire between the pins on the camera board and the Raspberry Pi.

1. Attach the tripod to the side tripod mount.

1. Assemble the rest of the ProtoStax case.

### Software

1. Make sure you can remotely access your Raspberry Pi over SSH. Note that if you bought a Raspberry Pi Zero (the one without Wi-Fi accessibilty) you will need to also buy an adapter of some sort, likely a micro-USB-to-Ethernet adapter.

1. Ensure that your Raspberry Pi can access the Internet.

1. Set up an SSH key for the Raspberry Pi on your computer and transfer the public key over to the Raspberry Pi.

1. Change the filepath to the SSH key in `ansible.cfg` for the entry `private_key_file`.

1. Change the hostname of the Raspberry Pi in `hosts.txt` if you opted to use something different. You should be able to use the `.local`-styled hostname instead of the actual IP address.

1. In `main.yml`, the field `remote_user` currently assumes you set the Raspberry Pi's username to the same username on your computer. If you did not do this, edit this field to match the username on the Raspberry Pi.

1. Run the Ansible playbook for setting up the Raspberry Pi.

    `ansible-playbook -K main.yml`

1. Open a port for port forwarding on your Wi-Fi router. Each Internet service provider (ISP) has a different router and interface to it than any other, so any tutorial on how to do this might not clarify everything you need to do. If the router settings only give you the option for one port number, then that port number will likely need to be the same on the Pi (check the `PORT` variable in `stream.py`). This port should not be one of the reserved ports used in Linux (generally anything below 1024).

1. If you didn't change the `cron` settings from the "Updating Raspberry Pi crontab" step of `main.yml`, the Raspberry Pi will start broadcasting the camera feed each time it starts up. You should be able to view the feed anywhere by entering the IP address and port number of your Wi-Fi router in a web browser in the format `http://<IP>:<PORT>`. If you don't see any feed in the web browser, check that you have the correct port number in `stream.py` and in your router settings and that the router isn't otherwise blocking it (e.g. firewall settings).

## Helpful Sources

- [Use Ansible to automate installation and deployment of Raspberry boxes](https://robertopozzi.medium.com/use-ansible-to-automate-installation-and-deployment-of-raspberry-boxes-cfe04ac10ce6)
- [Specify sudo password for Ansible](https://medium.com/@haroldfinch01/specify-sudo-password-for-ansible-1150e8bb19d7)
- [Raspberry Pi MJPEG Server Example](https://github.com/raspberrypi/picamera2/blob/main/examples/mjpeg_server.py)
    - The source code in this repo has been adapted from that found here.
