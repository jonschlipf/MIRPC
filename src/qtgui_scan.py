from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QMessageBox, QLineEdit, QMainWindow, QVBoxLayout,QHBoxLayout,QComboBox,QFileDialog
from PyQt5.QtCore import QThread,pyqtSignal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg,NavigationToolbar2QT

import time
import numpy as np
import matplotlib.pyplot as plt


class QtGuiScan(QVBoxLayout):
    def __init__(self,parent):
        super().__init__()
        self.parent=parent

        self.figure=plt.figure()
        self.canvas=FigureCanvasQTAgg(self.figure)
        self.toolbar=NavigationToolbar2QT(self.canvas,parent)

        self.scan_lmin_box=QLineEdit()
        self.scan_lmin_box.setText("500")
        self.scan_lstp_box=QLineEdit()
        self.scan_lstp_box.setText("50")
        self.scan_lmax_box=QLineEdit()
        self.scan_lmax_box.setText("800")
        self.scan_diode_button=QPushButton('Scan DUT')
        self.scan_diode_button.clicked.connect(self.measure_diode)
        self.scan_ref_button=QPushButton('Scan reference')
        self.scan_ref_button.clicked.connect(self.measure_ref)

        rangebar=QHBoxLayout()
        rangebar.addWidget(QLabel('l_min'))
        rangebar.addWidget(self.scan_lmin_box)
        rangebar.addWidget(QLabel('l_stp'))
        rangebar.addWidget(self.scan_lstp_box)
        rangebar.addWidget(QLabel('l_max'))
        rangebar.addWidget(self.scan_lmax_box)
        rangebar.addWidget(self.scan_diode_button)
        rangebar.addWidget(self.scan_ref_button)

        self.addWidget(self.toolbar)
        self.addWidget(self.canvas)
        self.addLayout(rangebar)

    def measure_diode(self):
        self.parent.lockin.set_input(1)
        self.parent.mono.set_wavelength(float(self.scan_lmin_box.text()))
        time.sleep(20*self.parent.lockin.get_timeconst())
        lam=np.arange(float(self.scan_lmin_box.text()),float(self.scan_lmax_box.text())+.01,float(self.scan_lstp_box.text()))
        self.thread=SpectrumThreadI(self,"I/A",self.parent.mono,self.parent.lockin,lam)
        self.thread._signal.connect(self.measure_diode_received)
        self.thread.start()
    def measure_diode_received(self,msg):
        self.canvas.draw()
        tosv=[]
        tosv.append(msg[0])
        tosv.append(msg[1])
        filename,filetype=QFileDialog.getSaveFileName(self.parent,"Save diode spectrum","./dut.csv","*.csv")
        try:
            np.savetxt(filename, np.array(tosv).T, delimiter=",",header="lambda/nm,I/A")
        except FileNotFoundError:
            pass
        self.parent.mono_layout.wavelength_box.setText("{:.2f}".format(self.parent.mono.get_wavelength()))
    def measure_ref(self):
        self.parent.lockin.set_input(0)
        self.parent.mono.set_wavelength(float(self.scan_lmin_box.text()))
        time.sleep(20*self.parent.lockin.get_timeconst())
        lam=np.arange(float(self.scan_lmin_box.text()),float(self.scan_lmax_box.text())+.01,float(self.scan_lstp_box.text()))
        self.thread=SpectrumThreadV(self,"V/V",self.parent.mono,self.parent.lockin,lam)
        self.thread._signal.connect(self.measure_ref_received)
        self.thread.start()
    def measure_ref_received(self,msg):
        tosv=[]
        tosv.append(msg[0])
        tosv.append(msg[1])
        filename,filetype=QFileDialog.getSaveFileName(self.parent,"Save reference spectrum","./reference.csv","*.csv")
        try:
            np.savetxt(filename, np.array(tosv).T, delimiter=",",header="lambda/nm,V/V")
        except FileNotFoundError:
            pass
        self.parent.mono_layout.wavelength_box.setText("{:.2f}".format(self.parent.mono.get_wavelength()))



class SpectrumThreadI(QThread):
    _signal=pyqtSignal(list)
    def __init__(self,caller,ylabel,mono,lockin,lam):
        super(SpectrumThreadI,self).__init__()
        self.parent=caller
        self.ylabel=ylabel
        self.mono=mono
        self.lockin=lockin
        self.lam=lam
    def __del__(self):
        self.wait()
    def run(self):
        data=0*self.lam
        for i in range(self.lam.size):
            print("set wl")
            print(self.lam[i])
            self.mono.set_wavelength(self.lam[i])
            print("wl set")
            time.sleep(2*self.lockin.get_timeconst())
            data[i]=self.lockin.get_R()
            print(data[i])
            self.parent.figure.clear()
            ax=self.parent.figure.add_subplot(111)
            ax.plot(self.lam[0:i+1],data[0:i+1],'*-')
            ax.set_xlabel("lambda / nm")
            ax.set_ylabel(self.ylabel)
            self.parent.canvas.draw()
        print("done")
        self._signal.emit([self.lam,data])

class SpectrumThreadV(QThread):
    _signal=pyqtSignal(list)
    def __init__(self,caller,ylabel,mono,lockin,lam):
        super(SpectrumThreadV,self).__init__()
        self.parent=caller
        self.ylabel=ylabel
        self.mono=mono
        self.lockin=lockin
        self.lam=lam
    def __del__(self):
        self.wait()
    def run(self):
        print(self.lam)
        data=0*self.lam
        for i in range(self.lam.size):
            print("set wl")
            print(self.lam[i])
            self.mono.set_wavelength(self.lam[i])
            print("wl set")
            time.sleep(2*self.lockin.get_timeconst())
            data[i]=self.lockin.get_Y()
            print(data[i])
            self.parent.figure.clear()
            ax=self.parent.figure.add_subplot(111)
            ax.plot(self.lam[0:i+1],data[0:i+1],'*-')
            ax.set_xlabel("lambda / nm")
            ax.set_ylabel(self.ylabel)
            self.parent.canvas.draw()
        print("done")
        self._signal.emit([self.lam,data])

