SETTINGS_PATH = r"~\Documents\Elemental Recycling\salvagEE\settings.ini"

# matplotlib setup
from matplotlib import use as mpl_backend
mpl_backend('QtAgg')

from PyQt6 import uic
from PyQt6.QtCore import QSettings
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QPushButton, QWidget
from os import path

from SalvageWindow import SalvageWindow

class MainWindow(QMainWindow):
    # Global Variables
    _baseDir = ''

    # Windows
    mainWindow: QWidget
    salvageWindow: SalvageWindow

    # Controls
    newSalvage_btn: QPushButton

    def __init__(self, baseDir:str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._baseDir = baseDir
        uic.loadUi(path.join(self._baseDir, 'app.ui'), self)

        self.mainWindow = self.centralWidget()
        self.salvageWindow = SalvageWindow(self._baseDir)

        self.newSalvage_btn.clicked.connect(self.onNewSalvage_clicked)
        self.salvageWindow.canceled.connect(self.onSalvageWindow_canceled)
        self.salvageWindow.saved.connect(self.onSalvageWindow_saved)

        try:
            self.loadConfig()
        except Exception as e:
            self.createPopupDialog('Warning', f'Failed to load settings. {e}')

    def onNewSalvage_clicked(self):
        self.mainWindow.setParent(None)
        self.setCentralWidget(self.salvageWindow)

    def onSalvageWindow_canceled(self):
        self.salvageWindow.setParent(None)
        self.setCentralWidget(self.mainWindow)

    def onSalvageWindow_saved(self):
        self.salvageWindow.setParent(None)
        self.setCentralWidget(self.mainWindow)

    def createPopupDialog(self, severity: str, message: str) -> bool:
        d = QMessageBox(self)
        d.setWindowTitle(severity)
        d.setText(message)
        if severity == 'Warning':
            d.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
            result = d.exec()
            return result == QMessageBox.StandardButton.Ok
        else:
            d.exec()
            return False

    def saveConfig(self):
        settings = QSettings(path.expanduser(SETTINGS_PATH), QSettings.Format.IniFormat)

    def loadConfig(self):
        settings = QSettings(path.expanduser(SETTINGS_PATH), QSettings.Format.IniFormat)

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            "Confirm Exit",
            "Are you sure you want to quit?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.saveConfig()
            event.accept()
        else:
            event.ignore()