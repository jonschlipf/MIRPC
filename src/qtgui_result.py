from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QMessageBox, QLineEdit, QMainWindow, QVBoxLayout,QHBoxLayout,QComboBox
from PyQt5.QtCore import QThread,pyqtSignal
import time

class QtGuiResult(QVBoxLayout):
    def __init__(self,lockin):
        super().__init__()
        self.lockin=lockin
        
        self.result_R_box=QLabel('blabla')
        self.result_phi_box=QLabel('blabla')
        self.result_R_box.setText("R={:f}".format(self.lockin.get_R()))
        self.result_phi_box.setText("phi={:f}°".format(self.lockin.get_phi()))
        self.result_update_button=QPushButton('Update result',self)
        self.result_update_button.clicked.connect(self.result_update_button_clicked)

        self.addWidget(QLabel('Lock-in data'))
        self.addWidget(self.result_R_box)
        self.addWidget(self.result_phi_box)
        self.addWidget(self.result_update_button)

        
    def result_update_button_clicked(self):
        time.sleep(.1)
        self.result_R_box.setText("R={:f}".format(self.lockin.get_R()))
        self.result_phi_box.setText("phi={:f}°".format(self.lockin.get_phi()))


