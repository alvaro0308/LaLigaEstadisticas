"""ConfigApp.py"""

import os
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QFileDialog


class ConfigAppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Abrir config.yaml")
        self.showMaximized()

        btn = QPushButton("Abrir fichero de configuración")
        layout = QVBoxLayout()
        layout.addWidget(btn)
        widget = QWidget()
        widget.setLayout(layout)
        widget.setAttribute(Qt.WA_DeleteOnClose)
        self.setCentralWidget(widget)

        btn.clicked.connect(self.open)

    def open(self):
        self.path = QFileDialog.getOpenFileName(self, 'Abrir config.yaml', '',
                                                'All Files (config.yaml)')
        self.close()

    def darkMode(self):
        """Apply dark mode to Application"""
        self.app.setStyle('Fusion')
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(15, 15, 15))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Highlight, QColor(0, 87, 184).lighter())
        palette.setColor(QPalette.HighlightedText, Qt.black)
        self.app.setPalette(palette)


class ConfigApp:
    def __init__(self):
        path = os.path.expanduser('~') + "/.laligaestadisticas"
        try:
            os.mkdir(path, 0o774)
        except:
            print(path + " already exists")

        pathFile = path + "/config.conf"

        if os.path.isfile(pathFile):
            f = open(pathFile, "r+")
        else:
            f = open(pathFile, "w+")

        line = f.readline()
        if "config.yaml" in line:
            print("Using cached configuration file at " + str(line))
            self.path = line
        else:
            self.app = QApplication(sys.argv)
            self.darkMode()
            configApp = ConfigAppWindow()
            self.app.exec_()
            self.path = configApp.path[0]
            f.write(self.path)
        f.close()

    def darkMode(self):
        """Apply dark mode to Application"""
        self.app.setStyle('Fusion')
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(15, 15, 15))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Highlight, QColor(0, 87, 184).lighter())
        palette.setColor(QPalette.HighlightedText, Qt.black)
        self.app.setPalette(palette)
