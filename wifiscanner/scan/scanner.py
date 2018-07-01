from wifi_interface import WifiInterface
from qualifier import Qualifier

class Scanner:
    def __init__(self, interface, ping_host):
        self.wifiInterface = WifiInterface(interface, ping_host)

    def __get_public_cells(self):
        cells = self.wifiInterface.getAllCells()
        publicCells = []

        for cell in cells:
            if cell.encrypted is not True:
                publicCells.append(cell)

        return publicCells

    def __get_working_cells(self, publicCells):
        workingCells = []

        try:
            for cell in publicCells:
                if self.wifiInterface.isCellOpenAndWorking(cell):
                    workingCells.append(cell)
        finally:
            #reboot the interface because the wifi module really fucks with it
            self.wifiInterface.reboot()

        return workingCells

    def get_open_cells(self):
        '''
        Retrieves all cells that are visible, open, and working
        '''
        publicCells = self.__get_public_cells()
        return self.__get_working_cells(publicCells)