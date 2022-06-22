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

#main window
class App(QWidget):

    def __init__(self,mono,lockin,stage):
        super().__init__()
        #register the instruments
        self.mono=mono
        self.lockin=lockin
        self.stage=stage
        #window title
        self.title='EFM MIR Photocurrent Control'
        self.setWindowTitle(self.title)

        #the widget for spectrum recording
        scan_layout=qtgui_scan.QtGuiScan(self)

        #the widget for constrol of the instruments
        instr_layout=QHBoxLayout()
        #first column is monochromator
        self.mono_layout=qtgui_mono.QtGuiMono(mono)
        instr_layout.addLayout(self.mono_layout)
        #second column is lock-in
        instr_layout.addLayout(qtgui_lockin.QtGuiLockin(lockin))
        #third column is sample stage (position, bias, etc.)
        stage_layout=qtgui_sample.QtGuiSample(lockin,stage,scan_layout.figure,scan_layout.canvas)
        instr_layout.addLayout(stage_layout)
        
        #vertical layout for the window, with scan/graph window above instrument control
        layout=QVBoxLayout()
        layout.addLayout(scan_layout)
        layout.addLayout(instr_layout)
        self.setLayout(layout)
        #make it visible
        self.show()
