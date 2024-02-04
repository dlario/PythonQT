#!/usr/bin/python3

from qgmap import *
import sys
from qgmap import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtSql import *
from PyQt6.uic import *

if __name__ == '__main__':

    def goCoords():
        def resetError():
            coordsEdit.setStyleSheet('')
        try: latitude, longitude = coordsEdit.text().split(",")
        except ValueError:
            coordsEdit.setStyleSheet("color: red;")
            QTimer.singleShot(500, resetError)
        else:
            gmap.centerAt(latitude, longitude)
            gmap.moveMarker("MyDragableMark", latitude, longitude)

    def goAddress():
        def resetError():
            addressEdit.setStyleSheet('')
            coords = gmap.centerAtAddress(addressEdit.text())
            if coords is None:
                addressEdit.setStyleSheet("color: red;")
                QTimer.singleShot(500, resetError)
                return
            gmap.moveMarker("MyDragableMark", *coords)
            coordsEdit.setText("{}, {}".format(*coords))

    def onMarkerMoved(key, latitude, longitude):
        print("Moved!!", key, latitude, longitude)
        coordsEdit.setText("{}, {}".format(latitude, longitude))
    def onMarkerRClick(key):
        print("RClick on ", key)
        gmap.setMarkerOptions(key, draggable=False)
    def onMarkerLClick(key):
        print("LClick on ", key)
    def onMarkerDClick(key):
        print("DClick on ", key)
        gmap.setMarkerOptions(key, draggable=True)

    def onMapMoved(latitude, longitude):
        print("Moved to ", latitude, longitude)
    def onMapRClick(latitude, longitude):
        print("RClick on ", latitude, longitude)
    def onMapLClick(latitude, longitude):
        print("LClick on ", latitude, longitude)
    def onMapDClick(latitude, longitude):
        print("DClick on ", latitude, longitude)

    app = QApplication(sys.argv)
    w = QDialog()
    h = QVBoxLayout(w)
    l = QFormLayout()
    h.addLayout(l)

    addressEdit = QLineEdit()
    l.addRow('Address:', addressEdit)
    addressEdit.editingFinished.connect(goAddress)
    coordsEdit = QLineEdit()
    l.addRow('Coords:', coordsEdit)
    coordsEdit.editingFinished.connect(goCoords)
    gmap = QGoogleMap(w)
    if 1==1:
        gmap.mapMoved.connect(onMapMoved)
        gmap.markerMoved.connect(onMarkerMoved)
        gmap.mapClicked.connect(onMapLClick)
        gmap.mapDoubleClicked.connect(onMapDClick)
        gmap.mapRightClicked.connect(onMapRClick)
        gmap.markerClicked.connect(onMarkerLClick)
        gmap.markerDoubleClicked.connect(onMarkerDClick)
        gmap.markerRightClicked.connect(onMarkerRClick)
    h.addWidget(gmap)
    gmap.setSizePolicy(
        QSizePolicy.MinimumExpanding,
        QSizePolicy.MinimumExpanding)
    w.show()

    gmap.waitUntilReady()
    coords = gmap.centerAtAddress("Jeffrey's Cafe Co. - 214 Place, 9909 102 St, Grande Prairie, AB T8V 2V4")

    if 1==1:
        gmap.centerAt(55.17, -118.80)
        gmap.setZoom(13)

        # Many icons at: https://sites.google.com/site/gmapsdevelopment/
        gmap.addMarker("MyDragableMark", *coords, **dict(icon="http://google.com/mapfiles/ms/micons/blue-dot.png",
                                                         draggable=True,
                                                         title = "Move me!"))

        # Some Static points
        for place in [
            "Jeffrey's Cafe Co. - 214 Place, 9909 102 St, Grande Prairie, AB T8V 2V4",
            "Kaymor Machining & Welding Ltd, 9703-72 Ave, Clairmont, AB T0H 0W0",
            ]:
            gmap.addMarkerAtAddress(place, icon="http://google.com/mapfiles/ms/micons/green-dot.png")
        gmap.setZoom(17)

    app.exec_()