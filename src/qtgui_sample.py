from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QMessageBox, QLineEdit, QMainWindow, QVBoxLayout,QHBoxLayout,QComboBox
from PyQt5.QtCore import QThread,pyqtSignal
import time

class QtGuiSample(QVBoxLayout):
    def __init__(self,lockin,stage):
        super().__init__()
        self.lockin=lockin
        self.stage=stage
        

        self.sample_bias_label=QLabel('DUT voltage bias / V')
        self.sample_bias_box=QLineEdit()
        self.sample_bias_box.setText("{:f}".format(self.lockin.get_bias()))
        self.sample_bias_button=QPushButton('Submit')
        self.sample_bias_button.clicked.connect(self.sample_bias_button_clicked)
        sample_bias_layout=QHBoxLayout()
        sample_bias_layout.addWidget(self.sample_bias_label)
        sample_bias_layout.addWidget(self.sample_bias_box)
        sample_bias_layout.addWidget(self.sample_bias_button)

        self.sample_irange_label=QLabel('DUT input current range / A')
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

        stagepos=self.stage.get_pos_mm()
        self.sample_x_label=QLabel('x / mm')
        self.sample_x_box=QLineEdit()
        self.sample_x_box.setText("{:f}".format(stagepos[0]))
        self.sample_y_label=QLabel('y / mm')
        self.sample_y_box=QLineEdit()
        self.sample_y_box.setText("{:f}".format(stagepos[1]))
        self.sample_z_label=QLabel('z / mm')
        self.sample_z_box=QLineEdit()
        self.sample_z_box.setText("{:f}".format(stagepos[2]))
        self.sample_pos_button=QPushButton('Submit')
        self.sample_pos_button.clicked.connect(self.sample_pos_button_clicked)
        sample_pos_layout=QHBoxLayout()
        sample_pos_layout.addWidget(self.sample_x_label)
        sample_pos_layout.addWidget(self.sample_x_box)
        sample_pos_layout.addWidget(self.sample_y_label)
        sample_pos_layout.addWidget(self.sample_y_box)
        sample_pos_layout.addWidget(self.sample_z_label)
        sample_pos_layout.addWidget(self.sample_z_box)
        sample_pos_layout.addWidget(self.sample_pos_button)
        
        self.sample_xmin_label=QLabel('x min')
        self.sample_xmin_box=QLineEdit()
        self.sample_xmin_box.setText("0")
        self.sample_xmax_label=QLabel('x max')
        self.sample_xmax_box=QLineEdit()
        self.sample_xmax_box.setText("0")
        self.sample_ymin_label=QLabel('y min')
        self.sample_ymin_box=QLineEdit()
        self.sample_ymin_box.setText("0")
        self.sample_ymax_label=QLabel('y max')
        self.sample_ymax_box=QLineEdit()
        self.sample_ymax_box.setText("0")
        self.sample_spcm_button=QPushButton('Map')
        self.sample_spcm_button.clicked.connect(self.sample_spcm_button_clicked)
        self.sample_opt_button=QPushButton('Maximize')
        self.sample_opt_button.clicked.connect(self.sample_opt_button_clicked)
        sample_min_layout=QHBoxLayout()
        sample_min_layout.addWidget(self.sample_xmin_label)
        sample_min_layout.addWidget(self.sample_xmin_box)
        sample_min_layout.addWidget(self.sample_ymin_label)
        sample_min_layout.addWidget(self.sample_ymin_box)
        sample_min_layout.addWidget(self.sample_spcm_button)
        sample_max_layout=QHBoxLayout()
        sample_max_layout.addWidget(self.sample_xmax_label)
        sample_max_layout.addWidget(self.sample_xmax_box)
        sample_max_layout.addWidget(self.sample_ymax_label)
        sample_max_layout.addWidget(self.sample_ymax_box)
        sample_max_layout.addWidget(self.sample_opt_button)


        self.addLayout(sample_bias_layout)
        self.addLayout(sample_irange_layout)
        self.addLayout(sample_pos_layout)
        self.addLayout(sample_min_layout)
        self.addLayout(sample_max_layout)
    def sample_spcm_button_clicked(self):
        pass
    def sample_opt_button_clicked(self):
        pass
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
        time.sleep(1)
        self.sample_irange_box.setText("{:f}".format(self.lockin.get_input_current_range()))
    def sample_bias_button_clicked(self):
        try:
            self.lockin.set_bias(float(self.sample_bias_box.text()))
        except ValueError:
            print("wrong type")
        time.sleep(.1)
        self.sample_bias_box.setText("{:f}".format(self.lockin.get_bias()))
    def sample_pos_button_clicked(self):
        self.stage.set_pos_mm(float(self.sample_x_box.text()),float(self.sample_y_box.text()),float(self.sample_z_box.text()))
        time.sleep(.1)
        stagepos=self.stage.get_pos_mm()
        self.sample_x_box.setText("{:f}".format(stagepos[0]))
        self.sample_y_box.setText("{:f}".format(stagepos[1]))
        self.sample_z_box.setText("{:f}".format(stagepos[2]))



