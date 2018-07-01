from wifi import Cell
from qualifier import Qualifier

class Scanner:
    def __init__(self, interface, ping_host):
        self.interface = interface
        self.ping_host = ping_host

    def __get_public_cells(self):
        cells = Cell.all(self.interface)

        publicCells = []
        for cell in cells:
            if cell.encrypted is not True:
                publicCells.append(cell)

        return publicCells

    def get_open_cells(self):
        publicCells = self.__get_public_cells()
        wifiQualifier = Qualifier(self.interface, self.ping_host)
        return wifiQualifier.get_working_cells(publicCells)