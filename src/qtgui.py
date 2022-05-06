from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QMessageBox, QLineEdit, QMainWindow, QVBoxLayout,QHBoxLayout,QComboBox
from PyQt5.QtCore import QThread,pyqtSignal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg,NavigationToolbar2QT
import matplotlib.pyplot as plt
import qtgui_mono
import qtgui_lockin
import qtgui_sample
import qtgui_scan
import qtgui_result
import time
import numpy as np


class App(QWidget):

    def __init__(self,mono,lockin):
        super().__init__()
        self.mono=mono
        self.lockin=lockin
        self.title='EFM MIR Photocurrent Control'
        self.setWindowTitle(self.title)

        instr_layout=QHBoxLayout()
        self.mono_layout=qtgui_mono.QtGuiMono(mono)
        instr_layout.addLayout(self.mono_layout)
        instr_layout.addLayout(qtgui_lockin.QtGuiLockin(lockin))
        instr_layout.addLayout(qtgui_sample.QtGuiSample(lockin))

        layout=QVBoxLayout()
        scan_layout=qtgui_scan.QtGuiScan(self)
        layout.addLayout(scan_layout)
        layout.addLayout(instr_layout)
        self.setLayout(layout)
        self.show()
