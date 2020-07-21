# Network Scanner (Raspberry PI)

This is a software for Raspberry Pi. It will scan your home network and notify you by mail when a new user enter in your network.
Probably join by a Django website to see all user and their activity.

## Requirements

Install nmap on your computer => [NMAP](https://nmap.org/)

**Archlinux**
```
sudo pacman -S nmap
```

**Debian/Ubuntu**
```
sudo apt install nmap
```

And of course python3.8 => [python](https://www.python.org/)

## Install

Create an **"/etc/Mail.json"** file to register your mail identification and SMTP server informations.

Use this template:
```
{
    "Port": <port number>,
    "SMTP_SSL": <SMTP url>,
    "Sender_Mail": <your mail>,
    "Receiver_Mail": <your mail>,
    "Password" : <your mail password>
}
```
Or see Template.json file.
