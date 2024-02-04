#!/usr/bin/python3
import sys
from qgmap import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtSql import *
from PyQt6.uic import *
from qgmap import *

if __name__ == '__main__':

    app = QApplication(sys.argv)
    w = QDialog()
    h = QVBoxLayout(w)
    l = QFormLayout()
    h.addLayout(l)

    addressEdit = QLineEdit()
    l.addRow('Address:', addressEdit)
    coordsEdit = QLineEdit()
    l.addRow('Coords:', coordsEdit)
    gmap = QGoogleMap(w)
    h.addWidget(gmap)
    gmap.setSizePolicy(
        QSizePolicy.MinimumExpanding,
        QSizePolicy.MinimumExpanding)
    w.show()

    gmap.waitUntilReady()


    app.exec_()