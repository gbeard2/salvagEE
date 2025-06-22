from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QComboBox, QHeaderView

from QFilePath import QFilePath


class SalvageTable(QTableWidget):
    schema = {
    'P/N': 'TEXT',
    'Type': 'TEXT',
    'Quantity': 'INTEGER',
    'Price': 'REAL',
    'Datasheet': 'TEXT'
    }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def getCellValue(self, row, col):
        widget = self.cellWidget(row, col)
        if widget:
            if isinstance(widget, QComboBox):
                return str(widget.currentText())
            elif isinstance(widget, QFilePath):
                return widget.text()
            else:
                return ''  # Unknown widget, ignore or customize here
        else:
            item = self.item(row, col)
            return item.text() if item else ''

    def addRow(self, data=None):
        row = self.rowCount()
        self.insertRow(row)

        data = data or ['', '', 0, 0.0, '']
        combo_items = ['Diode', 'PNP', 'NPN']

        # P/N: Alphanumeric
        item0 = QTableWidgetItem(str(data[0]))
        self.setItem(row, 0, item0)

        # Type: ComboBox
        combo = QComboBox()
        combo.addItems(combo_items)
        if data[1] in combo_items:
            combo.setCurrentText(data[1])
        self.setCellWidget(row, 1, combo)

        # Quantity: Integer
        item2 = QTableWidgetItem(str(int(data[2])))
        item2.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.setItem(row, 2, item2)

        # Price: Currency
        item3 = QTableWidgetItem(f'${float(data[3]):,.2f}')
        item3.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.setItem(row, 3, item3)

        # Datasheet: Filepath
        item4 = QFilePath(data[4])
        self.setCellWidget(row, 4, item4)
