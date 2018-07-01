import wifi
from urllib2 import urlopen, URLError, HTTPError
import subprocess

class WifiInterface:
    '''
    All interactions with the actual wifi interface should be done through this class
    '''

    def __init__(self, interface, ping_host):
        self.interface = interface
        self.ping_host = ping_host

    def getAllCells(self):
        '''
        Gets all publicly visible cells
        '''
        return wifi.Cell.all(self.interface)

    def isCellOpenAndWorking(self, cell):
        '''
        Attempts to connect to the wifi cell, and then attempts to ping a public host.
        If we cannot connect, or we cannot ping the host, return false.
        '''
        open = False
        scheme = wifi.Scheme.find(self.interface, "scraper")
        if scheme is None:
            scheme = wifi.Scheme.for_cell(self.interface, "scraper", cell)
            scheme.save()

        try:
            print("connecting to " + cell.ssid)
            scheme.activate()
            print("connected to " + cell.ssid)
            try :
                print("pinging " + self.ping_host)
                urlopen(self.ping_host)
            except HTTPError, e:
                print("failed to ping")
            except URLError, e:
                print("failed to ping")
            else :
                print("successful ping")
                open = True
        except wifi.exceptions.ConnectionError as e:
            print("failed to connect")

        return open

    def reboot(self):
        print("rebooting wireless interface")
        subprocess.call("sudo ifdown " + self.interface + " && sudo ifup " + self.interface, shell=True)
