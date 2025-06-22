import os

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtGui import QGuiApplication, QIcon, QPalette, QColor
from MainWindow import MainWindow
from ctypes import windll

if __name__ == "__main__":
    baseDir = os.path.dirname(__file__)
    windll.shell32.SetCurrentProcessExplicitAppUserModelID('com.Elemental Recycling.salvagEE')

    app = QApplication([])

    QGuiApplication.styleHints().setColorScheme(Qt.ColorScheme.Dark)
    palette = app.palette()
    palette.setColor(QPalette.ColorRole.Accent, QColor.fromString("#3399FF"))
    palette.setColor(QPalette.ColorRole.Highlight, QColor("#3399FF"))
    app.setPalette(palette)

    app.setWindowIcon(QIcon(os.path.join(baseDir, 'app.ico')))

    window = MainWindow(baseDir=baseDir)
    window.setWindowState(Qt.WindowState.WindowMaximized)
    window.show()

    try:
        app.exec()
    except Exception as e:
        d = QMessageBox()
        d.setWindowTitle("Error")
        d.setText(f"Failed to start application. {e}")
        d.exec()