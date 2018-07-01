import wifi
from urllib2 import urlopen, URLError, HTTPError
import subprocess

class Qualifier:
    def __init__(self, interface, ping_host):
        self.interface = interface
        self.ping_host = ping_host

    #for each, try to connect, and see if we actually have free wifi
    #(does it work? does it require browser login?)
    def get_working_cells(self, publicCells):
        workingCells = []
        try:
            for cell in publicCells:
                scheme = wifi.Scheme.find(self.interface, "scraper")
                if scheme is None:
                    scheme = wifi.Scheme.for_cell(self.interface, "scraper", cell)
                    scheme.save()
                print("connecting to " + cell.ssid)
                try:
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
                        workingCells.append(cell)
                except wifi.exceptions.ConnectionError as e:
                    print("failed to connect")
        finally:
            #reboot the interface because the wifi module really fucks with it
            print("rebooting wireless interface")
            subprocess.call("sudo ifdown " + self.interface + " && sudo ifup " + self.interface, shell=True)

        return workingCells