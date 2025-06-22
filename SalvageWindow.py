import sqlite3

from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QPushButton
from os import path

from SalvageTable import SalvageTable


class SalvageWindow(QWidget):
    _baseDir: str

    table: SalvageTable
    cancel_btn: QPushButton
    save_btn: QPushButton

    canceled = pyqtSignal()
    saved = pyqtSignal()

    def __init__(self, baseDir: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._baseDir = baseDir
        uic.loadUi(path.join(self._baseDir, 'salvage_window.ui'), self)

        self.table.addRow()

        self.cancel_btn.clicked.connect(self._onCancel_clicked)
        self.save_btn.clicked.connect(self._onSave_clicked)

    def _writeToDB(self):
        # Connect to DB
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        column_defs = ', '.join(f'\'{col}\' {typ}' for col, typ in self.table.schema.items())
        cursor.execute(f'DROP TABLE IF EXISTS Salvage')
        cursor.execute(f'CREATE TABLE Salvage ({column_defs})')

        # Insert rows
        for row in range(self.table.rowCount()):
            values = [self.table.getCellValue(row, col) for col in range(self.table.columnCount())]
            placeholders = ','.join('?' * len(values))
            cursor.execute(f'INSERT INTO Salvage VALUES ({placeholders})', values)

        conn.commit()
        conn.close()

    def _onCancel_clicked(self):
        self.canceled.emit()

    def _onSave_clicked(self):
        self._writeToDB()
        self.saved.emit()