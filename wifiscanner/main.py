from scan.scanner import Scanner
from archive.archiver import Archiver

def main():
    INTERFACE="wlan0"
    PING_HOST="http://www.google.com"
    SERVICE_ENDPOINT="http://47.35.153.175:8080/wifi"

    # scan for public cells
    scanner = Scanner(INTERFACE, PING_HOST)
    cells = scanner.get_open_cells()

    # archive cells
    archiver = Archiver(SERVICE_ENDPOINT)
    archiver.archive(cells)

if __name__ == "__main__":
    main()