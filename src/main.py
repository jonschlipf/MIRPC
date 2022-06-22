
import sys
import monochromator
import mfli
import stages
import time
import numpy as np
import qtgui
from PyQt5.QtWidgets import QApplication

#main class

#generated classes for all three instruments
mono=monochromator.Monochromator()
lockin=mfli.MFLI()
stage=stages.Stage3()

#launch Qt GUI
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex=qtgui.App(mono,lockin,stage)
    sys.exit(app.exec_())

