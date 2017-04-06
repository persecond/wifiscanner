#pip install wifi
import wifi
import pprint
import socket
from urllib2 import urlopen, URLError, HTTPError
import requests
import json
import subprocess

interface="wlan0"
ping_host="http://www.google.com"
service_endpoint="http://47.35.153.175:8080/wifi"

#get the good stuff
def get_public_cells():
    cells = wifi.Cell.all(interface)

    publicCells = []
    for cell in cells:
        if cell.encrypted is not True:
            publicCells.append(cell)

    return publicCells


def post_cell(cell):
    prettyprint = pprint.PrettyPrinter(indent=4)
    
    data = {}
    data["ssid"] = cell.ssid
    data["signal"] = cell.signal
    data["quality"] = cell.quality
    data["frequency"] = cell.frequency
    #data["bitrates"] = cell.bitrates
    data["encrypted"] = cell.encrypted
    data["channel"] = cell.channel
    data["address"] = cell.address
    data["mode"] = cell.mode

    headers = {'Content-type': 'application/json'}

    print("posting cell to " + service_endpoint)
    r = requests.post(service_endpoint, data=json.dumps(data), headers=headers)
    print("response was " + str(r.status_code))
    print(prettyprint.pprint(json.dumps(data)))

#for each, try to connect, and see if we actually have free wifi
#(does it work? does it require browser login?)
def get_working_cells():
    publicCells = get_public_cells()
    
    try:
        for cell in publicCells:
            scheme = wifi.Scheme.find(interface, "scraper")
            if scheme is None:
                scheme = Scheme.for_cell(interface, "scraper", cell)
                scheme.save()
            print("connecting to " + cell.ssid)
            try:
                scheme.activate()
                print("connected to " + cell.ssid)
                print("pinging " + ping_host)
                try :
                    response = urlopen( ping_host )
                except HTTPError, e:
                    print("failed to ping")
                except URLError, e:
                    print("failed to ping")
                else :
                    html = response.read()
                    print("successful ping")

                    post_cell(cell)
            except wifi.exceptions.ConnectionError as e:
                print("failed to connect")
    finally:
        #reboot the interface because the wifi module really fucks with it
        print("rebooting wireless interface")
        subprocess.call("sudo ifdown " + interface + " && sudo ifup " + interface, shell=True)

class TestCell:
    ssid = "test"
    signal = "test"
    quality = "test"
    frequency = "test"
    bitrates = "test"
    encrypted = "test"
    channel = "test"
    address = "test"
    mode = "test"

cells = get_public_cells()
for cell in cells:
    post_cell(cell)
