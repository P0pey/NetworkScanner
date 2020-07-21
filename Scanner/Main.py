#!/usr/bin/python
#Author: Popey

##################################
#           Import               #
##################################

import socket, json, os
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
def update(db):
    db = set_disconnect(db)
    hosts = minidom.parse('/tmp/res')
    ip = hosts.getElementsByTagName('address')
    name = hosts.getElementsByTagName('hostname')
    for i in range(len(ip)):
        find = False
        j = 0
        while j < len(db['Hosts']) and not find:
            if db['Hosts'][j]['IP'] == ip[i].attributes['addr'].value:
                db['Hosts'][j]['connect'] = 1
                find = True
            j += 1
        if not find:
            db['Hosts'].append({
                'Name': name[i].attributes['name'].value,
                'IP': ip[i].attributes['addr'].value,
                'IP_Type': ip[i].attributes['addrtype'].value,
                'connect': 1
            })
    return db

# Save database in a JSON file
def save(db):
    with open('/tmp/Hosts.txt', 'w') as outfile:
        json.dump(db, outfile, indent=4)

##################################
#              Run               #
##################################

if __name__ == "__main__":

    #Remove nmap res file
    if os.path.isfile('/tmp/res'):
        os.remove('/tmp/res')

    database = get_data()
    # Remove databse file
    if os.path.isfile('/tmp/Hosts.txt'):
        os.remove('/tmp/Hosts.txt')

    ip = get_IP()
    get_connected_hosts(ip)
    database = update(database)
    save(database)
