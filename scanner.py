import wifi

class Scanner:
    def __init__(self, interface):
        self.interface = interface

    def get_public_cells(self):
        cells = wifi.Cell.all(self.interface)

        publicCells = []
        for cell in cells:
            if cell.encrypted is not True:
                publicCells.append(cell)

        return publicCells