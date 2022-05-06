
import sys
import monochromator
import mfli
import time
import numpy as np
import qtgui
from PyQt5.QtWidgets import QApplication

mono=monochromator.Monochromator()
lockin=mfli.MFLI()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex=qtgui.App(mono,lockin)
    sys.exit(app.exec_())

