from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QMessageBox, QLineEdit, QMainWindow, QVBoxLayout,QHBoxLayout,QComboBox
from PyQt5.QtCore import QThread,pyqtSignal
import time

class QtGuiSample(QVBoxLayout):
    def __init__(self,lockin):
        super().__init__()
        self.lockin=lockin
        

        self.sample_bias_label=QLabel('DUT voltage bias / V')
        self.sample_bias_box=QLineEdit()
        self.sample_bias_box.setText("{:f}".format(self.lockin.get_bias()))
        self.sample_bias_button=QPushButton('Submit')
        self.sample_bias_button.clicked.connect(self.sample_bias_button_clicked)
        sample_bias_layout=QHBoxLayout()
        sample_bias_layout.addWidget(self.sample_bias_label)
        sample_bias_layout.addWidget(self.sample_bias_box)
        sample_bias_layout.addWidget(self.sample_bias_button)

        self.sample_irange_label=QLabel('DUT input current range / I')
        self.sample_irange_box=QLineEdit()
        self.sample_irange_box.setText("{:f}".format(self.lockin.get_input_current_range()))
        self.sample_irange_button=QPushButton('Submit')
        self.sample_irange_button.clicked.connect(self.sample_irange_button_clicked)
        self.sample_irange_auto_button=QPushButton('Auto')
        self.sample_irange_auto_button.clicked.connect(self.sample_irange_auto_button_clicked)
        sample_irange_layout=QHBoxLayout()
        sample_irange_layout.addWidget(self.sample_irange_label)
        sample_irange_layout.addWidget(self.sample_irange_box)
        sample_irange_layout.addWidget(self.sample_irange_button)
        sample_irange_layout.addWidget(self.sample_irange_auto_button)

        self.addLayout(sample_bias_layout)
        self.addLayout(sample_irange_layout)
    def sample_irange_button_clicked(self):
        try:
            self.lockin.set_input_current_range(float(self.sample_irange_box.text()))
        except ValueError:
            print("wrong type")
        time.sleep(.1)
        self.sample_irange_box.setText("{:f}".format(self.lockin.get_input_current_range()))
    def sample_irange_auto_button_clicked(self):
        try:
            self.lockin.auto_input_current_range()
        except ValueError:
            print("wrong type")
        time.sleep(10)
        self.sample_irange_box.setText("{:f}".format(self.lockin.get_input_current_range()))
    def sample_bias_button_clicked(self):
        try:
            self.lockin.set_bias(float(self.sample_bias_box.text()))
        except ValueError:
            print("wrong type")
        time.sleep(.1)
        self.sample_bias_box.setText("{:f}".format(self.lockin.get_bias()))



