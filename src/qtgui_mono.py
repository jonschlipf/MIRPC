from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QMessageBox, QLineEdit, QMainWindow, QVBoxLayout,QHBoxLayout,QComboBox
from PyQt5.QtCore import QThread,pyqtSignal
import time

#gui buttons to control the ihr320 monochromator
class QtGuiMono(QVBoxLayout):
    def __init__(self,mono):
        super().__init__()

        self.mono=mono
        #see manual for explanation
        self.grating_label=QLabel('Grating')
        self.grating_box=QComboBox()
        self.grating_box.addItems(['G1','G2','G3'])
        self.grating_box.setCurrentIndex(self.mono.get_grating())
        self.grating_box.currentIndexChanged.connect(self.grating_changed)
        mono_grating_layout=QHBoxLayout()
        mono_grating_layout.addWidget(self.grating_label)
        mono_grating_layout.addWidget(self.grating_box)

        self.wavelength_label=QLabel('Wavelength λ / nm')
        self.wavelength_box=QLineEdit()
        self.wavelength_box.setText("{:.2f}".format(self.mono.get_wavelength()))
        self.wavelength_button=QPushButton('Submit')
        self.wavelength_button.clicked.connect(self.wavelength_button_clicked)
        mono_wl_layout=QHBoxLayout()
        mono_wl_layout.addWidget(self.wavelength_label)
        mono_wl_layout.addWidget(self.wavelength_box)
        mono_wl_layout.addWidget(self.wavelength_button)

        self.filter_label=QLabel('Filter')
        self.filter_box=QComboBox()
        self.filter_box.addItems(['Auto','F1 : UV-S1','F2 : 1.0µm longpass','F3 : 1.9ṃ longpass','F4 : 3.5µm longpass','F5 : None','F6 : None'])
        self.filter_box.setCurrentIndex(self.mono.get_filter())
        self.filter_box.currentIndexChanged.connect(self.filter_changed)
        mono_filter_layout=QHBoxLayout()
        mono_filter_layout.addWidget(self.filter_label)
        mono_filter_layout.addWidget(self.filter_box)

        self.entr_slit_label=QLabel('Entrance slit')
        self.entr_slit_box=QLineEdit()
        self.entr_slit_box.setText(str(self.mono.get_entr_slit()))
        self.entr_slit_button=QPushButton('Submit')
        self.entr_slit_button.clicked.connect(self.entr_slit_button_clicked)
        mono_entr_slit_layout=QHBoxLayout()
        mono_entr_slit_layout.addWidget(self.entr_slit_label)
        mono_entr_slit_layout.addWidget(self.entr_slit_box)
        mono_entr_slit_layout.addWidget(self.entr_slit_button)

        self.exit_slit_label=QLabel('Exit slit')
        self.exit_slit_box=QLineEdit()
        self.exit_slit_box.setText(str(self.mono.get_exit_slit()))
        self.exit_slit_button=QPushButton('Submit')
        self.exit_slit_button.clicked.connect(self.exit_slit_button_clicked)
        mono_exit_slit_layout=QHBoxLayout()
        mono_exit_slit_layout.addWidget(self.exit_slit_label)
        mono_exit_slit_layout.addWidget(self.exit_slit_box)
        mono_exit_slit_layout.addWidget(self.exit_slit_button)

        
        self.addLayout(mono_grating_layout)
        self.addLayout(mono_wl_layout)
        self.addLayout(mono_filter_layout)
        self.addLayout(mono_entr_slit_layout)
        self.addLayout(mono_exit_slit_layout)
    #process button inputs to directly set hardware properties
    def wavelength_button_clicked(self):
        try:
            self.mono.set_wavelength(float(self.wavelength_box.text()))
        except ValueError:
            print("wrong type")
        self.wavelength_box.setText("{:.2f}".format(self.mono.get_wavelength()))
    def grating_changed(self,i):
        try:
            self.mono.set_grating(int(i))
        except ValueError:
            print("wrong type")
    def filter_changed(self,i):
        try:
            self.mono.set_filter(int(i))
        except ValueError:
            print("wrong type")
    def entr_slit_button_clicked(self):
        try:
            self.mono.set_entr_slit(float(self.entr_slit_box.text()))
        except ValueError:
            print("wrong type")
        self.entr_slit_box.setText(str(self.mono.get_entr_slit()))
    def exit_slit_button_clicked(self):
        try:
            self.mono.set_exit_slit(float(self.exit_slit_box.text()))
        except ValueError:
            print("wrong type")
        self.exit_slit_box.setText(str(self.mono.get_exit_slit()))


