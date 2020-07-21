#!/usr/bin/python
#Author: Popey

##################################
#           Import               #
##################################

import socket, json, os, time, smtplib
from xml.dom import minidom

##################################
#           Scripts              #
##################################

# Open the database (JSON)
def get_data():
    if os.path.isfile('/tmp/Hosts.txt'):
        with open('/tmp/Hosts.txt') as json_file:
            data = json.load(json_file)
        return data
    data = {}
    data['Hosts'] = []
    return data

# Get your local ip address != 127.0.1.1
def get_IP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    my_ip = s.getsockname()[0]
    s.close()
    return my_ip

# NMAP scan (get all host connect on the same network)
def get_connected_hosts(IP):
    command = 'nmap -sn ' + IP + '/24 -oX /tmp/res'
    os.system(command)

# Just put all databse ip down
def set_disconnect(db):
    for i in range(len(db['Hosts'])):
        db['Hosts'][i]['connect'] = 0
    return db

# Update the database with new ip
def update(db, time_date):
    db = set_disconnect(db)
    hosts = minidom.parse('/tmp/res')
    ip = hosts.getElementsByTagName('address')
    name = hosts.getElementsByTagName('hostname')
    New = []
    for i in range(len(ip)):
        find = False
        j = 0
        while j < len(db['Hosts']) and not find:
            if db['Hosts'][j]['IP'] == ip[i].attributes['addr'].value:
                db['Hosts'][j]['connect'] = 1
                db['Hosts'][j]['Time'] = time_date
                find = True
            j += 1
        if not find:
            db['Hosts'].append({
                'Name': name[i].attributes['name'].value,
                'IP': ip[i].attributes['addr'].value,
                'IP_Type': ip[i].attributes['addrtype'].value,
                'Time': time_date,
                'connect': 1
            })
            New.append((ip[i].attributes['addr'].value, name[i].attributes['name'].value))
    if len(New) > 0:
        send_mail(New)
    return db

# Send a notification when there is a new connection
def send_mail(List):
    with open('/etc/Mail.json') as json_file:
        data = json.load(json_file)

    message = ""
    l = len(List)
    if l == 1:
        message = "1 new connection => IP: " + List[0][0] + ' & Name: ' + List[0][1]
    else:
        message = str(l) + " new connections"
        i = 1
        for ip, name in List:
            if i < l:
                message += str(i) + '=> IP: ' + ip + ' & Name: ' + name + '\n'
            else:
                message += str(i) + '=> IP: ' + ip + ' & Name: ' + name
            i += 1

    server = smtplib.SMTP(data['SMTP_SSL'], data['Port'])
    server.starttls()
    server.login(data['Sender_Mail'], data['Password'])
    server.sendmail(data['Sender_Mail'], data['Receiver_Mail'], message)
    server.quit()

# Save database in a JSON file
def save(db):
    with open('/tmp/Hosts.txt', 'w') as outfile:
        json.dump(db, outfile, indent=4)

##################################
#              Run               #
##################################

if __name__ == "__main__":

    # Generate Output date
    time_tmp = time.localtime(time.time())
    year = str(time_tmp[0])
    month = str(time_tmp[1])
    day = str(time_tmp[2])
    hour = str(time_tmp[3])
    minute = str(time_tmp[4])
    seconde = str(time_tmp[5])
    time_date = year + '-' + month + '-' + day + ' ' + hour + ':' + minute + ':' + seconde

    #Remove nmap res file
    if os.path.isfile('/tmp/res'):
        os.remove('/tmp/res')

    database = get_data()
    # Remove databse file
    if os.path.isfile('/tmp/Hosts.txt'):
        os.remove('/tmp/Hosts.txt')

    ip = get_IP()
    get_connected_hosts(ip)
    database = update(database, time_date)
    save(database)
