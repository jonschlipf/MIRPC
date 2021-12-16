import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QMessageBox, QLineEdit, QMainWindow, QVBoxLayout,QHBoxLayout,QComboBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg,NavigationToolbar2QT
import matplotlib.pyplot as plt
import random
import monochromator

mono=monochromator.Monochromator()

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title='EFM MIR Photocurrent Control'
        self.setWindowTitle(self.title)

        self.figure=plt.figure()
        self.canvas=FigureCanvasQTAgg(self.figure)
        self.toolbar=NavigationToolbar2QT(self.canvas,self)
        self.scan_button=QPushButton('Scan',self)
        self.scan_button.clicked.connect(self.plot)

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
        self.wavelength_box.setText(str(mono.get_wavelength()))
        self.wavelength_button=QPushButton('Submit',self)
        self.wavelength_button.clicked.connect(self.wavelength_button_clicked)
        mono_wl_layout=QHBoxLayout()
        mono_wl_layout.addWidget(self.wavelength_label)
        mono_wl_layout.addWidget(self.wavelength_box)
        mono_wl_layout.addWidget(self.wavelength_button)

        self.filter_label=QLabel('Filter')
        self.filter_box=QComboBox(self)
        self.filter_box.addItems(['Auto','F1','F2','F3','F4','F5','F6'])
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

        instr_layout=QHBoxLayout()
        instr_layout.addLayout(mono_layout)

        layout=QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.scan_button)
        layout.addLayout(instr_layout)
        self.setLayout(layout)
        self.show()

    def plot(self):
        data=[random.random() for i in range(10)]
        self.figure.clear()
        ax=self.figure.add_subplot(111)
        ax.plot(data,'*-')
        self.canvas.draw()
    def wavelength_button_clicked(self):
        try:
            mono.set_wavelength(float(self.wavelength_box.text()))
        except ValueError:
            print("wrong type")
        self.wavelength_box.setText(str(mono.get_wavelength()))
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

    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex=App()
    sys.exit(app.exec_())
