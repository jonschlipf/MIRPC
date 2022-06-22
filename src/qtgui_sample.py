from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QMessageBox, QLineEdit, QMainWindow, QVBoxLayout,QHBoxLayout,QComboBox
from PyQt5.QtCore import QThread,pyqtSignal
import time
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

class QtGuiSample(QVBoxLayout):
    def __init__(self,lockin,stage,figure,canvas):
        super().__init__()
        self.lockin=lockin
        self.stage=stage
        self.figure=figure
        self.canvas=canvas
        

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
        self.sample_xstp_label=QLabel('x step')
        self.sample_xstp_box=QLineEdit()
        self.sample_xstp_box.setText("1")
        self.sample_xmax_label=QLabel('x max')
        self.sample_xmax_box=QLineEdit()
        self.sample_xmax_box.setText("20")
        self.sample_ymin_label=QLabel('y min')
        self.sample_ymin_box=QLineEdit()
        self.sample_ymin_box.setText("0")
        self.sample_ystp_label=QLabel('y step')
        self.sample_ystp_box=QLineEdit()
        self.sample_ystp_box.setText("2")
        self.sample_ymax_label=QLabel('y max')
        self.sample_ymax_box=QLineEdit()
        self.sample_ymax_box.setText("50")
        self.sample_spcm_button=QPushButton('Map')
        self.sample_spcm_button.clicked.connect(self.sample_spcm_button_clicked)
        self.sample_opt_button=QPushButton('Maximize')
        self.sample_opt_button.clicked.connect(self.sample_opt_button_clicked)

        sample_x_layout=QHBoxLayout()
        sample_x_layout.addWidget(self.sample_xmin_label)
        sample_x_layout.addWidget(self.sample_xmin_box)
        sample_x_layout.addWidget(self.sample_xstp_label)
        sample_x_layout.addWidget(self.sample_xstp_box)
        sample_x_layout.addWidget(self.sample_xmax_label)
        sample_x_layout.addWidget(self.sample_xmax_box)
        sample_x_layout.addWidget(self.sample_spcm_button)
        sample_y_layout=QHBoxLayout()
        sample_y_layout.addWidget(self.sample_ymin_label)
        sample_y_layout.addWidget(self.sample_ymin_box)
        sample_y_layout.addWidget(self.sample_ystp_label)
        sample_y_layout.addWidget(self.sample_ystp_box)
        sample_y_layout.addWidget(self.sample_ymax_label)
        sample_y_layout.addWidget(self.sample_ymax_box)
        sample_y_layout.addWidget(self.sample_opt_button)


        self.addLayout(sample_bias_layout)
        self.addLayout(sample_irange_layout)
        self.addLayout(sample_pos_layout)
        self.addLayout(sample_x_layout)
        self.addLayout(sample_y_layout)
    def sample_spcm_button_clicked(self):
        print("map acquisition")
        self.lockin.set_input(1)
        #set pos init
        #time.sleep(20*self.lockin.get_timeconst())
        xrange=np.arange(float(self.sample_xmin_box.text()),float(self.sample_xmax_box.text())+1e-5,float(self.sample_xstp_box.text()))
        yrange=np.arange(float(self.sample_ymin_box.text()),float(self.sample_ymax_box.text())+1e-5,float(self.sample_ystp_box.text()))
        self.thread=XYThread(self,self.stage,self.lockin,xrange,yrange)
        self.thread._signal.connect(self.measure_xy_received)
        self.thread.start()
    def measure_xy_received(self,msg):
        pass
    def opt_received(self,msg):
        spos=self.stage.get_pos_mm()
        self.stage.set_pos_mm(msg[0],msg[1],spos[2])
        
        
    def sample_opt_button_clicked(self):
        self.lockin.set_input(1)
        startval=[.5*(float(self.sample_xmin_box.text())+float(self.sample_xmax_box.text())),.5*(float(self.sample_ymin_box.text())+float(self.sample_ymax_box.text()))]
        self.thread=OptThread(self,self.stage,self.lockin,startval)
        self.thread._signal.connect(self.opt_received)
        self.thread.start()
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

class XYThread(QThread):
    _signal=pyqtSignal(list)
    def __init__(self,caller,stage,lockin,xrange,yrange):
        super(XYThread,self).__init__()
        self.parent=caller
        self.stage=stage
        self.lockin=lockin
        self.xrange=xrange
        self.yrange=yrange
    def __del__(self):
        self.wait()
    def run(self):
        spos=self.stage.get_pos_mm()
        data=np.zeros((self.yrange.size,self.xrange.size))
        print("scanning")
        for i1 in range(self.xrange.size):
            for i2 in range(self.yrange.size):
                self.stage.set_pos_mm(self.xrange[i1],self.yrange[i2],spos[2])
                time.sleep(10*self.lockin.get_timeconst())
                data[i2,i1]=self.lockin.get_R()
                print([self.xrange[i1],self.yrange[i2]])
            self.parent.figure.clear()
            ax=self.parent.figure.add_subplot(111)
            ax.pcolor(self.xrange[0:i1+1],self.yrange,data[:,0:i1+1])
            #ax.colorbar()
            ax.set_xlabel("x / mm")
            ax.set_ylabel("y / mm")
            self.parent.canvas.draw()
        print("XY scan done")
        self._signal.emit([self.xrange])

class OptThread(QThread):
    _signal=pyqtSignal(list)
    def __init__(self,caller,stage,lockin,startval):
        super(OptThread,self).__init__()
        self.parent=caller
        self.stage=stage
        self.lockin=lockin
        self.startval=startval
        print(startval)
    def __del__(self):
        self.wait()
    def run(self):
        spos=self.stage.get_pos_mm()
        def objective(xy):
            self.stage.set_pos_mm(xy[0],xy[1],spos[2])
            time.sleep(10*self.lockin.get_timeconst())
            print(xy)
            print(self.lockin.get_R())
            return 1/self.lockin.get_R()

        result=minimize(objective,self.startval,method='nelder-mead',xatol=.01)
        result=result.x
        print(result)
        print("XY scan done")
        self._signal.emit([result])
