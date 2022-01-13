import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QMessageBox, QLineEdit, QMainWindow, QVBoxLayout,QHBoxLayout,QComboBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg,NavigationToolbar2QT
import matplotlib.pyplot as plt
import random
import monochromator
import mfli
import time
import numpy as np

mono=monochromator.Monochromator()
lockin=mfli.MFLI()

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title='EFM MIR Photocurrent Control'
        self.setWindowTitle(self.title)

        self.figure=plt.figure()
        self.canvas=FigureCanvasQTAgg(self.figure)
        self.toolbar=NavigationToolbar2QT(self.canvas,self)

        self.grating_label=QLabel('Grating')
        self.grating_box=QComboBox(self)
        self.grating_box.addItems(['G1','G2','G3'])
        self.grating_box.setCurrentIndex(mono.get_grating())
        self.grating_box.currentIndexChanged.connect(self.grating_changed)
        mono_grating_layout=QHBoxLayout()
        mono_grating_layout.addWidget(self.grating_label)
        mono_grating_layout.addWidget(self.grating_box)

        self.wavelength_label=QLabel('Wavelength λ / nm')
        self.wavelength_box=QLineEdit(self)
        self.wavelength_box.setText("{:.2f}".format(mono.get_wavelength()))
        self.wavelength_button=QPushButton('Submit',self)
        self.wavelength_button.clicked.connect(self.wavelength_button_clicked)
        mono_wl_layout=QHBoxLayout()
        mono_wl_layout.addWidget(self.wavelength_label)
        mono_wl_layout.addWidget(self.wavelength_box)
        mono_wl_layout.addWidget(self.wavelength_button)

        self.filter_label=QLabel('Filter')
        self.filter_box=QComboBox(self)
        self.filter_box.addItems(['Auto','F1 : UV-S1','F2 : 1.0µm longpass','F3 : 1.9ṃ longpass','F4 : 3.5µm longpass','F5 : None','F6 : None'])
        self.filter_box.setCurrentIndex(mono.get_filter())
        self.filter_box.currentIndexChanged.connect(self.filter_changed)
        mono_filter_layout=QHBoxLayout()
        mono_filter_layout.addWidget(self.filter_label)
        mono_filter_layout.addWidget(self.filter_box)

        self.entr_slit_label=QLabel('Entrance slit')
        self.entr_slit_box=QLineEdit(self)
        self.entr_slit_box.setText(str(mono.get_entr_slit()))
        self.entr_slit_button=QPushButton('Submit',self)
        self.entr_slit_button.clicked.connect(self.entr_slit_button_clicked)
        mono_entr_slit_layout=QHBoxLayout()
        mono_entr_slit_layout.addWidget(self.entr_slit_label)
        mono_entr_slit_layout.addWidget(self.entr_slit_box)
        mono_entr_slit_layout.addWidget(self.entr_slit_button)

        self.exit_slit_label=QLabel('Exit slit')
        self.exit_slit_box=QLineEdit(self)
        self.exit_slit_box.setText(str(mono.get_exit_slit()))
        self.exit_slit_button=QPushButton('Submit',self)
        self.exit_slit_button.clicked.connect(self.exit_slit_button_clicked)
        mono_exit_slit_layout=QHBoxLayout()
        mono_exit_slit_layout.addWidget(self.exit_slit_label)
        mono_exit_slit_layout.addWidget(self.exit_slit_box)
        mono_exit_slit_layout.addWidget(self.exit_slit_button)

        mono_layout=QVBoxLayout()
        mono_layout.addLayout(mono_grating_layout)
        mono_layout.addLayout(mono_wl_layout)
        mono_layout.addLayout(mono_filter_layout)
        mono_layout.addLayout(mono_entr_slit_layout)
        mono_layout.addLayout(mono_exit_slit_layout)

        self.oscillator_label=QLabel('Oscillator frequency f / Hz')
        self.oscillator_box=QLineEdit(self)
        self.oscillator_box.setText("{:.2f}".format(lockin.get_oscillator()))
        self.oscillator_button=QPushButton('Submit',self)
        self.oscillator_button.clicked.connect(self.oscillator_button_clicked)
        lockin_oscillator_layout=QHBoxLayout()
        lockin_oscillator_layout.addWidget(self.oscillator_label)
        lockin_oscillator_layout.addWidget(self.oscillator_box)
        lockin_oscillator_layout.addWidget(self.oscillator_button)

        self.lockin_harmonic_label=QLabel('Lock-in harmonic')
        self.lockin_harmonic_box=QLineEdit(self)
        self.lockin_harmonic_box.setText("{:.0f}".format(lockin.get_harmonic()))
        self.lockin_harmonic_button=QPushButton('Submit',self)
        self.lockin_harmonic_button.clicked.connect(self.lockin_harmonic_button_clicked)
        lockin_harmonic_layout=QHBoxLayout()
        lockin_harmonic_layout.addWidget(self.lockin_harmonic_label)
        lockin_harmonic_layout.addWidget(self.lockin_harmonic_box)
        lockin_harmonic_layout.addWidget(self.lockin_harmonic_button)

        self.lockin_order_label=QLabel('Lock-in LPF order')
        self.lockin_order_box=QLineEdit(self)
        self.lockin_order_box.setText("{:.0f}".format(lockin.get_order()))
        self.lockin_order_button=QPushButton('Submit',self)
        self.lockin_order_button.clicked.connect(self.lockin_order_button_clicked)
        lockin_order_layout=QHBoxLayout()
        lockin_order_layout.addWidget(self.lockin_order_label)
        lockin_order_layout.addWidget(self.lockin_order_box)
        lockin_order_layout.addWidget(self.lockin_order_button)

        self.lockin_timeconst_label=QLabel('Lock-in LPF time constant t / s')
        self.lockin_timeconst_box=QLineEdit(self)
        self.lockin_timeconst_box.setText("{:f}".format(lockin.get_timeconst()))
        self.lockin_timeconst_button=QPushButton('Submit',self)
        self.lockin_timeconst_button.clicked.connect(self.lockin_timeconst_button_clicked)
        lockin_timeconst_layout=QHBoxLayout()
        lockin_timeconst_layout.addWidget(self.lockin_timeconst_label)
        lockin_timeconst_layout.addWidget(self.lockin_timeconst_box)
        lockin_timeconst_layout.addWidget(self.lockin_timeconst_button)

        self.lockin_vrange_label=QLabel('Reference detector voltage range / V')
        self.lockin_vrange_box=QLineEdit(self)
        self.lockin_vrange_box.setText("{:f}".format(lockin.get_input_voltage_range()))
        self.lockin_vrange_button=QPushButton('Submit',self)
        self.lockin_vrange_button.clicked.connect(self.lockin_vrange_button_clicked)
        self.lockin_vrange_auto_button=QPushButton('Auto',self)
        self.lockin_vrange_auto_button.clicked.connect(self.lockin_vrange_auto_button_clicked)
        lockin_vrange_layout=QHBoxLayout()
        lockin_vrange_layout.addWidget(self.lockin_vrange_label)
        lockin_vrange_layout.addWidget(self.lockin_vrange_box)
        lockin_vrange_layout.addWidget(self.lockin_vrange_button)
        lockin_vrange_layout.addWidget(self.lockin_vrange_auto_button)

        lockin_layout=QVBoxLayout()
        lockin_layout.addLayout(lockin_oscillator_layout)
        lockin_layout.addLayout(lockin_harmonic_layout)
        lockin_layout.addLayout(lockin_order_layout)
        lockin_layout.addLayout(lockin_timeconst_layout)
        lockin_layout.addLayout(lockin_vrange_layout)

        self.sample_bias_label=QLabel('DUT voltage bias / V')
        self.sample_bias_box=QLineEdit(self)
        self.sample_bias_box.setText("{:f}".format(lockin.get_bias()))
        self.sample_bias_button=QPushButton('Submit',self)
        self.sample_bias_button.clicked.connect(self.sample_bias_button_clicked)
        sample_bias_layout=QHBoxLayout()
        sample_bias_layout.addWidget(self.sample_bias_label)
        sample_bias_layout.addWidget(self.sample_bias_box)
        sample_bias_layout.addWidget(self.sample_bias_button)

        self.sample_irange_label=QLabel('DUT input current range / I')
        self.sample_irange_box=QLineEdit(self)
        self.sample_irange_box.setText("{:f}".format(lockin.get_input_current_range()))
        self.sample_irange_button=QPushButton('Submit',self)
        self.sample_irange_button.clicked.connect(self.sample_irange_button_clicked)
        self.sample_irange_auto_button=QPushButton('Auto',self)
        self.sample_irange_auto_button.clicked.connect(self.sample_irange_auto_button_clicked)
        sample_irange_layout=QHBoxLayout()
        sample_irange_layout.addWidget(self.sample_irange_label)
        sample_irange_layout.addWidget(self.sample_irange_box)
        sample_irange_layout.addWidget(self.sample_irange_button)
        sample_irange_layout.addWidget(self.sample_irange_auto_button)

        sample_layout=QVBoxLayout()
        sample_layout.addLayout(sample_bias_layout)
        sample_layout.addLayout(sample_irange_layout)

        instr_layout=QHBoxLayout()
        instr_layout.addLayout(mono_layout)
        instr_layout.addLayout(lockin_layout)
        instr_layout.addLayout(sample_layout)


        self.result_R_box=QLabel('blabla')
        self.result_phi_box=QLabel('blabla')
        self.result_R_box.setText("R={:f}".format(lockin.get_R()))
        self.result_phi_box.setText("phi={:f}°".format(lockin.get_phi()))
        self.result_update_button=QPushButton('Update result',self)
        self.result_update_button.clicked.connect(self.result_update_button_clicked)

        result_layout=QHBoxLayout()
        result_layout.addWidget(QLabel('Lock-in data'))
        result_layout.addWidget(self.result_R_box)
        result_layout.addWidget(self.result_phi_box)
        result_layout.addWidget(self.result_update_button)

        self.scan_lmin_box=QLineEdit(self)
        self.scan_lmin_box.setText("500")
        self.scan_lstp_box=QLineEdit(self)
        self.scan_lstp_box.setText("50")
        self.scan_lmax_box=QLineEdit(self)
        self.scan_lmax_box.setText("800")
        self.scan_diode_button=QPushButton('Scan DUT',self)
        self.scan_diode_button.clicked.connect(self.measure_diode)
        self.scan_ref_button=QPushButton('Scan reference',self)
        self.scan_ref_button.clicked.connect(self.measure_ref)

        scan_layout=QHBoxLayout()
        scan_layout.addWidget(QLabel('l_min'))
        scan_layout.addWidget(self.scan_lmin_box)
        scan_layout.addWidget(QLabel('l_stp'))
        scan_layout.addWidget(self.scan_lstp_box)
        scan_layout.addWidget(QLabel('l_max'))
        scan_layout.addWidget(self.scan_lmax_box)
        scan_layout.addWidget(self.scan_diode_button)
        scan_layout.addWidget(self.scan_ref_button)


        layout=QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addLayout(scan_layout)
        layout.addLayout(result_layout)
        layout.addLayout(instr_layout)
        self.setLayout(layout)
        self.show()



    def measure_diode(self):
        lockin.set_input(1)
        mono.set_wavelength(float(self.scan_lmin_box.text()))
        time.sleep(20*lockin.get_timeconst())
        lam=np.arange(float(self.scan_lmin_box.text()),float(self.scan_lmax_box.text()),float(self.scan_lstp_box.text()))
        print(lam)
        data=[random.random() for i in range(lam.size)]
        for i in range(lam.size):
            print("set wl")
            print(lam[i])
            mono.set_wavelength(lam[i])
            print("wl set")
            time.sleep(10*lockin.get_timeconst())
            data[i]=lockin.get_R()
            print(data[i])
            self.figure.clear()
            ax=self.figure.add_subplot(111)
            ax.plot(lam,data,'*-')
            self.canvas.draw()
        print("done")
        self.wavelength_box.setText(str(mono.get_wavelength()))
        tosv=[]
        tosv.append(lam)
        tosv.append(data)
        np.savetxt("diode.csv", np.array(tosv).T, delimiter=",",header="lambda/nm,I/A")
    def measure_ref(self):
        lockin.set_input(0)
        mono.set_wavelength(float(self.scan_lmin_box.text()))
        time.sleep(20*lockin.get_timeconst())
        lam=np.arange(float(self.scan_lmin_box.text()),float(self.scan_lmax_box.text()),float(self.scan_lstp_box.text()))
        print(lam)
        data=[random.random() for i in range(lam.size)]
        for i in range(lam.size):
            print("set wl")
            print(lam[i])
            mono.set_wavelength(lam[i])
            print("wl set")
            time.sleep(10*lockin.get_timeconst())
            data[i]=lockin.get_R()
            print(data[i])
            self.figure.clear()
            ax=self.figure.add_subplot(111)
            ax.plot(lam,data,'*-')
            self.canvas.draw()
        print("done")
        self.wavelength_box.setText("{:.2f}".format(mono.get_wavelength()))
        tosv=[]
        tosv.append(lam)
        tosv.append(data)
        np.savetxt("reference.csv", np.array(tosv).T, delimiter=",",header="lambda/nm,V/V")
    def wavelength_button_clicked(self):
        try:
            mono.set_wavelength(float(self.wavelength_box.text()))
        except ValueError:
            print("wrong type")
        self.wavelength_box.setText("{:.2f}".format(mono.get_wavelength()))
    def grating_changed(self,i):
        try:
            mono.set_grating(int(i))
        except ValueError:
            print("wrong type")
    def filter_changed(self,i):
        try:
            mono.set_filter(int(i))
        except ValueError:
            print("wrong type")
    def entr_slit_button_clicked(self):
        try:
            mono.set_entr_slit(float(self.entr_slit_box.text()))
        except ValueError:
            print("wrong type")
        self.entr_slit_box.setText(str(mono.get_entr_slit()))
    def exit_slit_button_clicked(self):
        try:
            mono.set_exit_slit(float(self.exit_slit_box.text()))
        except ValueError:
            print("wrong type")
        self.exit_slit_box.setText(str(mono.get_exit_slit()))
    def oscillator_button_clicked(self):
        try:
            lockin.set_oscillator(float(self.oscillator_box.text()))
        except ValueError:
            print("wrong type")
        time.sleep(.1)
        self.oscillator_box.setText("{:.2f}".format(lockin.get_oscillator()))
    def lockin_harmonic_button_clicked(self):
        try:
            lockin.set_harmonic(float(self.lockin_harmonic_box.text()))
        except ValueError:
            print("wrong type")
        time.sleep(.1)
        self.lockin_harmonic_box.setText("{:.0f}".format(lockin.get_harmonic()))
    def lockin_timeconst_button_clicked(self):
        try:
            lockin.set_timeconst(float(self.lockin_timeconst_box.text()))
        except ValueError:
            print("wrong type")
        time.sleep(.1)
        self.lockin_timeconst_box.setText("{:f}".format(lockin.get_timeconst()))
    def lockin_order_button_clicked(self):
        try:
            lockin.set_order(int(self.lockin_order_box.text()))
        except ValueError:
            print("wrong type")
        time.sleep(.1)
        self.lockin_order_box.setText("{:.0f}".format(lockin.get_order()))

    def result_update_button_clicked(self):
        time.sleep(.1)
        self.result_R_box.setText("R={:f}".format(lockin.get_R()))
        self.result_phi_box.setText("phi={:f}°".format(lockin.get_phi()))

    def lockin_vrange_button_clicked(self):
        try:
            lockin.set_input_voltage_range(float(self.lockin_vrange_box.text()))
        except ValueError:
            print("wrong type")
        time.sleep(.1)
        self.lockin_vrange_box.setText("{:f}".format(lockin.get_input_voltage_range()))
    def lockin_vrange_auto_button_clicked(self):
        try:
            lockin.auto_input_voltage_range()
        except ValueError:
            print("wrong type")
        time.sleep(10)
        self.lockin_vrange_box.setText("{:f}".format(lockin.get_input_voltage_range()))
    def sample_irange_button_clicked(self):
        try:
            lockin.set_input_current_range(float(self.sample_irange_box.text()))
        except ValueError:
            print("wrong type")
        time.sleep(.1)
        self.sample_irange_box.setText("{:f}".format(lockin.get_input_current_range()))
    def sample_irange_auto_button_clicked(self):
        try:
            lockin.auto_input_current_range()
        except ValueError:
            print("wrong type")
        time.sleep(10)
        self.sample_irange_box.setText("{:f}".format(lockin.get_input_current_range()))
    def sample_bias_button_clicked(self):
        try:
            lockin.set_bias(float(self.sample_bias_box.text()))
        except ValueError:
            print("wrong type")
        time.sleep(.1)
        self.sample_bias_box.setText("{:f}".format(lockin.get_bias()))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex=App()
    sys.exit(app.exec_())
