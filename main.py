from scanner import Scanner
from qualifier import Qualifier
from archiver import Archiver

INTERFACE="wlan0"
PING_HOST="http://www.google.com"
SERVICE_ENDPOINT="http://47.35.153.175:8080/wifi"

# scan for public cells
scanner = Scanner(INTERFACE)
cells = scanner.get_public_cells()

# determine what cells are working
qualifer = Qualifier(INTERFACE, PING_HOST)
workingCells = qualifer.get_working_cells(cells)

# archive cells
archiver = Archiver(SERVICE_ENDPOINT)
archiver.post_cells(workingCells)
