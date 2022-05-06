from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QMessageBox, QLineEdit, QMainWindow, QVBoxLayout,QHBoxLayout,QComboBox
from PyQt5.QtCore import QThread,pyqtSignal
import time

class QtGuiLockin(QVBoxLayout):
    def __init__(self,lockin):
        super().__init__()
        self.lockin=lockin
        self.oscillator_label=QLabel('Oscillator frequency f / Hz')
        self.oscillator_box=QLineEdit()
        self.oscillator_box.setText("{:.2f}".format(self.lockin.get_oscillator()))
        self.oscillator_button=QPushButton('Submit')
        self.oscillator_button.clicked.connect(self.oscillator_button_clicked)
        lockin_oscillator_layout=QHBoxLayout()
        lockin_oscillator_layout.addWidget(self.oscillator_label)
        lockin_oscillator_layout.addWidget(self.oscillator_box)
        lockin_oscillator_layout.addWidget(self.oscillator_button)

        self.lockin_harmonic_label=QLabel('Lock-in harmonic')
        self.lockin_harmonic_box=QLineEdit()
        self.lockin_harmonic_box.setText("{:.0f}".format(self.lockin.get_harmonic()))
        self.lockin_harmonic_button=QPushButton('Submit')
        self.lockin_harmonic_button.clicked.connect(self.lockin_harmonic_button_clicked)
        lockin_harmonic_layout=QHBoxLayout()
        lockin_harmonic_layout.addWidget(self.lockin_harmonic_label)
        lockin_harmonic_layout.addWidget(self.lockin_harmonic_box)
        lockin_harmonic_layout.addWidget(self.lockin_harmonic_button)

        self.lockin_order_label=QLabel('Lock-in LPF order')
        self.lockin_order_box=QLineEdit()
        self.lockin_order_box.setText("{:.0f}".format(self.lockin.get_order()))
        self.lockin_order_button=QPushButton('Submit')
        self.lockin_order_button.clicked.connect(self.lockin_order_button_clicked)
        lockin_order_layout=QHBoxLayout()
        lockin_order_layout.addWidget(self.lockin_order_label)
        lockin_order_layout.addWidget(self.lockin_order_box)
        lockin_order_layout.addWidget(self.lockin_order_button)

        self.lockin_timeconst_label=QLabel('Lock-in LPF time constant t / s')
        self.lockin_timeconst_box=QLineEdit()
        self.lockin_timeconst_box.setText("{:f}".format(self.lockin.get_timeconst()))
        self.lockin_timeconst_button=QPushButton('Submit')
        self.lockin_timeconst_button.clicked.connect(self.lockin_timeconst_button_clicked)
        lockin_timeconst_layout=QHBoxLayout()
        lockin_timeconst_layout.addWidget(self.lockin_timeconst_label)
        lockin_timeconst_layout.addWidget(self.lockin_timeconst_box)
        lockin_timeconst_layout.addWidget(self.lockin_timeconst_button)

        self.lockin_vrange_label=QLabel('Reference detector voltage range / V')
        self.lockin_vrange_box=QLineEdit()
        self.lockin_vrange_box.setText("{:f}".format(self.lockin.get_input_voltage_range()))
        self.lockin_vrange_button=QPushButton('Submit')
        self.lockin_vrange_button.clicked.connect(self.lockin_vrange_button_clicked)
        self.lockin_vrange_auto_button=QPushButton('Auto')
        self.lockin_vrange_auto_button.clicked.connect(self.lockin_vrange_auto_button_clicked)
        lockin_vrange_layout=QHBoxLayout()
        lockin_vrange_layout.addWidget(self.lockin_vrange_label)
        lockin_vrange_layout.addWidget(self.lockin_vrange_box)
        lockin_vrange_layout.addWidget(self.lockin_vrange_button)
        lockin_vrange_layout.addWidget(self.lockin_vrange_auto_button)

        self.addLayout(lockin_oscillator_layout)
        self.addLayout(lockin_harmonic_layout)
        self.addLayout(lockin_order_layout)
        self.addLayout(lockin_timeconst_layout)
        self.addLayout(lockin_vrange_layout)
    def oscillator_button_clicked(self):
        try:
            self.lockin.set_oscillator(float(self.oscillator_box.text()))
        except ValueError:
            print("wrong type")
        time.sleep(.1)
        self.oscillator_box.setText("{:.2f}".format(self.lockin.get_oscillator()))
    def lockin_harmonic_button_clicked(self):
        try:
            self.lockin.set_harmonic(float(self.lockin_harmonic_box.text()))
        except ValueError:
            print("wrong type")
        time.sleep(.1)
        self.lockin_harmonic_box.setText("{:.0f}".format(self.lockin.get_harmonic()))
    def lockin_timeconst_button_clicked(self):
        try:
            self.lockin.set_timeconst(float(self.lockin_timeconst_box.text()))
        except ValueError:
            print("wrong type")
        time.sleep(.1)
        self.lockin_timeconst_box.setText("{:f}".format(self.lockin.get_timeconst()))
    def lockin_order_button_clicked(self):
        try:
            self.lockin.set_order(int(self.lockin_order_box.text()))
        except ValueError:
            print("wrong type")
        time.sleep(.1)
        self.lockin_order_box.setText("{:.0f}".format(self.lockin.get_order()))


    def lockin_vrange_button_clicked(self):
        try:
            self.lockin.set_input_voltage_range(float(self.lockin_vrange_box.text()))
        except ValueError:
            print("wrong type")
        time.sleep(.1)
        self.lockin_vrange_box.setText("{:f}".format(self.lockin.get_input_voltage_range()))
    def lockin_vrange_auto_button_clicked(self):
        try:
            self.lockin.auto_input_voltage_range()
        except ValueError:
            print("wrong type")
        time.sleep(10)    
        self.lockin_vrange_box.setText("{:f}".format(self.lockin.get_input_voltage_range()))





