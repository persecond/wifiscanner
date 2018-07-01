import requests
import json
import pprint

class Archiver:
    def __init__(self, service_endpoint):
        self.service_endpoint = service_endpoint

    def post_cell(self, cell):
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

        print("posting cell to " + self.service_endpoint)
        r = requests.post(self.service_endpoint, data=json.dumps(data), headers=headers)
        print("response was " + str(r.status_code))
        print(prettyprint.pprint(json.dumps(data)))

    def archive(self, cells):
        for cell in cells:
            self.post_cell(cell)