## Copyright 2023 David Lario
__author__ = 'David Lario'
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at

##     http://www.apache.org/licenses/LICENSE-2.0

## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.

## Revision History
## October 27, 2023 - David James Lario - Created

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PackageManager.Packages.ProgramBase.UI.Forms.TextEditor import richtextlineedit
import numpy as np
import random
from qimage2ndarray import array2qimage

class GenericDelegate(QItemDelegate):

    def __init__(self, parent=None):
        super(GenericDelegate, self).__init__(parent)
        self.delegates = {}


    def insertColumnDelegate(self, column, delegate):
        delegate.setParent(self)
        self.delegates[column] = delegate


    def removeColumnDelegate(self, column):
        if column in self.delegates:
            del self.delegates[column]


    def paint(self, painter, option, index):
        delegate = self.delegates.get(index.column())
        if delegate is not None:
            delegate.paint(painter, option, index)
        else:
            QItemDelegate.paint(self, painter, option, index)


    def createEditor(self, parent, option, index):
        delegate = self.delegates.get(index.column())
        if delegate is not None:
            return delegate.createEditor(parent, option, index)
        else:
            return QItemDelegate.createEditor(self, parent, option,
                                              index)
    def setEditorData(self, editor, index):
        editor.blockSignals(True)
        delegate = self.delegates.get(index.column())
        if delegate is not None:
            delegate.setEditorData(editor, index)
        else:
            QItemDelegate.setEditorData(self, editor, index)
        editor.blockSignals(False)

    def setModelData(self, editor, model, index):
        delegate = self.delegates.get(index.column())
        if delegate is not None:
            delegate.setModelData(editor, model, index)
        else:
            QItemDelegate.setModelData(self, editor, model, index)

    def flags(self, index):
        if (index.column() == 0):
            return Qt.ItemIsEditable | Qt.ItemIsEnabled
        else:
            return Qt.ItemIsEnabled

class ButtonDelegate(QItemDelegate):

    def __init__(self, parent):
        QItemDelegate.__init__(self, parent)

    def createEditor(self, parent, option, index):
        combo = QPushButton(str(index.data()), parent)

        #self.connect(combo, QtCore.SIGNAL("currentIndexChanged(int)"), self, QtCore.SLOT("currentIndexChanged()"))
        combo.clicked.connect(self.currentIndexChanged)
        return combo

    def setEditorData(self, editor, index):
        editor.blockSignals(True)
        #editor.setCurrentIndex(int(index.model().data(index)))
        editor.blockSignals(False)

    def setModelData(self, editor, model, index):
        model.setData(index, editor.text())

    @Slot()
    def currentIndexChanged(self):
        self.commitData.emit(self.sender())

class ComboDelegate(QStyledItemDelegate):
    def __init__(self, parent, dataModel):
        super(ComboDelegate, self).__init__(parent)
        self.dataListModel = dataModel
        self.parent = parent

    def createEditor(self, parent, option, index):
        self.editor = QComboBox(parent)
        self.editor.setModel(self.dataListModel)
        self.editor.setModelColumn(1)
        #self.editor.setEditable(True)
        #self.editor.installEventFilter(self)
        self.editor.currentIndexChanged[str].connect(self.on_editor_currentIndexChanged)
        #The one below works to for some reason too
        #self.editor.currentIndexChanged.connect(self.on_editor_currentIndexChanged1)

        return self.editor

    def setEditorData(self, editor, index):
        self.editor.blockSignals(True)
        #a = str(editor.model().index(2,1).data())
        #b = index.model().data(index)
        #c = index.data(Qt.DisplayRole)

        #print(a,b,c)
        value = index.model().data(index, Qt.EditRole)
        #print(value)
        #self.editor.setCurrentIndex(-1)
        #self.editor.setCurrentIndex(self.editor.findText(index.data(Qt.DisplayRole)))
        if value is not None:
            for row in range(editor.model().rowCount(None)):
                if str(self.editor.model().index(row,1).data()) == index.data(Qt.DisplayRole):
                    self.editor.setCurrentIndex(row)
                    break

        self.editor.blockSignals(False)

    def setModelData(self, editor, model, index):
        model.setData(index, editor.currentIndex())

    @Slot(int)
    def on_editor_currentIndexChanged(self, index):
        print("Combo Index changed {0} {1} : {2}".format(index, self.sender().currentIndex(), self.sender().currentText()))
        self.commitData.emit(self.sender())

class QColorButton(QPushButton):
    '''
    Custom Qt Widget to show a chosen color.

    Left-clicking the button shows the color-chooser, while
    right-clicking resets the color to None (no-color).    
    '''

    colorChanged = Signal()

    def __init__(self, *args, **kwargs):
        super(QColorButton, self).__init__(*args, **kwargs)

        self._color = None
        self.setMaximumWidth(32)
        self.pressed.connect(self.onColorPicker)

    def setColor(self, color):
        if color != self._color:
            self._color = color
            self.colorChanged.emit()

        if self._color:
            self.setStyleSheet("background-color: %s;" % self._color)
        else:
            self.setStyleSheet("")

    def color(self):
        return self._color

    def onColorPicker(self):
        '''
        Show color-picker dialog to select color.

        Qt will use the native dialog by default.

        '''
        dlg = QColorDialog(self)
        if self._color:
            dlg.setCurrentColor(QColor(self._color))

        if dlg.exec_():
            self.setColor(dlg.currentColor().name())

    def mousePressEvent(self, e):
        if e.button() == Qt.RightButton:
            self.setColor(None)

        return super(QColorButton, self).mousePressEvent(e)

class CheckBoxDelegate(QStyledItemDelegate):
    """
    A delegate that places a fully functioning QCheckBox in every
    cell of the column to which it's applied
    """
    def __init__(self, parent):
        QItemDelegate.__init__(self, parent)

    def createEditor(self, parent, option, index):
        '''
        Important, otherwise an editor is created if the user clicks in this cell.
        ** Need to hook up a signal to the model
        '''
        return None

    def paint(self, painter, option, index):
        '''
        Paint a checkbox without the label.
        '''

        checked = bool(index.data()) #.toBool()
        check_box_style_option = QStyleOptionButton()

        #index.flags() &
        if (Qt.ItemIsEditable) > 0:
            check_box_style_option.state |= QStyle.State_Enabled
        else:
            check_box_style_option.state |= QStyle.State_ReadOnly

        if checked:
            check_box_style_option.state |= QStyle.State_On
        else:
            check_box_style_option.state |= QStyle.State_Off

        check_box_style_option.rect = self.getCheckBoxRect(option)

        # this will not run - hasFlag does not exist
        #if not index.model().hasFlag(index, QtCore.Qt.ItemIsEditable):
            #check_box_style_option.state |= QStyle.State_ReadOnly

        check_box_style_option.state |= QStyle.State_Enabled

        QApplication.style().drawControl(QStyle.CE_CheckBox, check_box_style_option, painter)

    def editorEvent(self, event, model, option, index):
        '''
        Change the data in the model and the state of the checkbox
        if the user presses the left mousebutton or presses
        Key_Space or Key_Select and this cell is editable. Otherwise do nothing.
        '''
        print('Check Box editor Event detected : ')
        #print (event.type()) #index.flags()
        if not (Qt.ItemIsEditable) > 0:
            return False

        print('Check Box editor Event detected : passed first check')
        # Do not change the checkbox-state
        if event.type() == QEvent.MouseButtonPress:
          return False
        if event.type() == QEvent.MouseButtonRelease or event.type() == QEvent.MouseButtonDblClick:
            if event.button() != Qt.LeftButton or not self.getCheckBoxRect(option).contains(event.pos()):
                return False
            if event.type() == QEvent.MouseButtonDblClick:
                return True
        elif event.type() == QEvent.KeyPress:
            if event.key() != Qt.Key_Space and event.key() != Qt.Key_Select:
                return False
            else:
                return False

        # Change the checkbox-state
        self.setModelData(None, model, index)
        return True

    def setModelData (self, editor, model, index):
        '''
        The user wanted to change the old state in the opposite.
        '''
        print('SetModelData')
        newValue = not bool(index.data()) #.toBool()
        print('New Value : {0}'.format(newValue))
        model.setData(index, newValue, Qt.EditRole)

    def getCheckBoxRect(self, option):
        check_box_style_option = QStyleOptionButton()
        check_box_rect = QApplication.style().subElementRect(QStyle.SE_CheckBoxIndicator, check_box_style_option, None)
        check_box_point = QPoint (option.rect.x() +
                            option.rect.width() / 2 -
                            check_box_rect.width() / 2,
                            option.rect.y() +
                            option.rect.height() / 2 -
                            check_box_rect.height() / 2)
        return QRect(check_box_point, check_box_rect.size())

class SpinColumnDelegate(QStyledItemDelegate):
    def __init__(self, minimum=0, maximum=100, parent=None):
        super(IntegerColumnDelegate, self).__init__(parent)
        self.minimum = minimum
        self.minimum = minimum
        self.maximum = maximum

    def createEditor(self, parent, option, index):
        sbox = QSpinBox(parent)
        sbox.setRange(0, 100)
        return sbox

    def setEditorData(self, editor, index):
        item_var = index.data(Qt.DisplayRole)
        item_str = item_var.toPyObject()
        item_int = int(item_str)
        editor.setValue(item_int)

    def setModelData(self, editor, model, index):
        data_int = editor.value()
        data_var = data_int
        model.setData(index, data_var)

class IntegerColumnDelegate(QItemDelegate):

    def __init__(self, minimum=0, maximum=100, parent=None):
        super(IntegerColumnDelegate, self).__init__(parent)
        self.minimum = minimum
        self.maximum = maximum


    def createEditor(self, parent, option, index):
        spinbox = QSpinBox(parent)
        spinbox.setRange(self.minimum, self.maximum)
        spinbox.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        return spinbox


    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.DisplayRole).toInt()[0]
        editor.setValue(value)

    def setModelData(self, editor, model, index):
        editor.interpretText()
        model.setData(index, editor.value())

class DateColumnDelegate(QItemDelegate):

    def __init__(self, minimum=QDate(), maximum=QDate.currentDate(),
                 format="yyyy-MM-dd", parent=None):
        super(DateColumnDelegate, self).__init__(parent)
        self.minimum = minimum
        self.maximum = maximum
        self.format = str(format)


    def createEditor(self, parent, option, index):
        dateedit = QDateEdit(parent)
        dateedit.setDateRange(self.minimum, self.maximum)
        dateedit.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        dateedit.setDisplayFormat(self.format)
        dateedit.setCalendarPopup(True)
        return dateedit


    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.DisplayRole).toDate()
        editor.setDate(value)


    def setModelData(self, editor, model, index):
        model.setData(index, editor.date())


class PlainTextColumnDelegate(QItemDelegate):

    def __init__(self, parent=None):
        super(PlainTextColumnDelegate, self).__init__(parent)


    def createEditor(self, parent, option, index):
        lineedit = QLineEdit(parent)
        return lineedit


    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.DisplayRole).toString()
        editor.setText(value)


    def setModelData(self, editor, model, index):
        model.setData(index, editor.text())


class RichTextColumnDelegate(QItemDelegate):

    def __init__(self, parent=None):
        super(RichTextColumnDelegate, self).__init__(parent)


    def paint(self, painter, option, index):
        text = index.model().data(index, Qt.DisplayRole)
        palette = QApplication.palette()
        document = QTextDocument()
        document.setDefaultFont(option.font)
        if option.state & QStyle.State_Selected:
            pass
            #document.setHtml(str("<font color=%1>%2</font>") \
             #       .arg(palette.highlightedText().color().name()) \
             #       .arg(text))
        else:
            document.setHtml(text)
        painter.save()
        color = palette.highlight().color() \
            if option.state & QStyle.State_Selected \
            else QColor(index.model().data(index,
                    Qt.BackgroundColorRole))
        painter.fillRect(option.rect, color)
        painter.translate(option.rect.x(), option.rect.y())
        document.drawContents(painter)
        painter.restore()


    def sizeHint(self, option, index):
        text = index.model().data(index)
        document = QTextDocument()
        document.setDefaultFont(option.font)
        document.setHtml(text)
        return QSize(document.idealWidth() + 5,
                     option.fontMetrics.height())


    def createEditor(self, parent, option, index):
        lineedit = richtextlineedit.RichTextLineEdit(parent)
        return lineedit


    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.DisplayRole)
        editor.setHtml(value)


    def setModelData(self, editor, model, index):
        model.setData(index, editor.toSimpleHtml())

class IconComboBox(QComboBox):
    def __init__(self,iconFileName, parent=None):
        super(IconComboBox,self).__init__(parent)
        colorList=['yellow','red','blue','green']

        for color in colorList:
            pix=QPixmap(QSize(20,20))
            pix.fill(QColor(color))
            pix = QPixmap(iconFileName)
            self.addItem(QIcon(pix),color)

class CellObject(object):
    cell_index = {}

    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.backgroundcolor = Qt.white
        self.foregroundcolor = Qt.black
        self.image = None
        self.combolist = []

        CellObject.cell_index[str(str(self.row) + "," + str(self.column))] = self

    @classmethod
    def find_by_cell(cls, row, column):
        return CellDetails.cell_index[str(self.row,",",self.column)]


class CustomStyledDelegate(QStyledItemDelegate):
    #Need to set the image location
    def __init__(self, parent, celldict):
        super(CustomStyledDelegate, self).__init__(parent)
        self.celldict = celldict

    def paint(self,painter,option, index):
        #painter.save()

        # set background color
        painter.setPen(QPen(Qt.NoPen))
        #stuff it does when selected.
        if option.state & QStyle.State_Selected:
            painter.fillRect(option.rect, Qt.white)
            try:
                if self.celldict[str(str(index.row()) + "," + str(index.column()))].image is not None:
                    # path = "path\to\my\image.jpg"
                    self.CreateImage()
                    path = self.imageLocation

                    image = QImage(self.imageLocation)
                    pixmap = QPixmap.fromImage(self.Image)
                    pixmap.scaled(50, 40, Qt.KeepAspectRatio)
                    painter.drawPixmap(option.rect, pixmap)
            except:
                pass
        else:
            try:
                if self.celldict[str(str(index.row()) + "," + str(index.column()))] is not None:
                    forecolor = self.celldict[str(str(index.row()) + "," + str(index.column()))].foregroundcolor
                    backgroundcolor = self.celldict[str(str(index.row()) + "," + str(index.column()))].backgroundcolor
                    background = QLinearGradient(0, 0, 10, 0)
                    background.setColorAt(0.00, backgroundcolor)
                    background.setColorAt(0.99, QColor('#d0d0d0'))
                    background.setColorAt(1.00, QColor('#f8f8f8'))

                    #painter.setBrush(QBrush(background))
                    #painter.setBrush(QBrush(QColor(backgroundcolor)))
                    painter.setBrush(QBrush(backgroundcolor))
            except:
                painter.setBrush(QBrush(Qt.white))


        painter.drawRect(option.rect)

        #Set Text Color
        painter.setPen(QPen(Qt.black))
        value = index.data(Qt.DisplayRole)
        if value != None:
            text = str(value)
            painter.drawText(option.rect, Qt.AlignLeft, text)

        #line = QLine( option.rect.topLeft(), option.rect.topRight() )
        #painter.drawLine( line )

        painter.restore()

    def createEditor(self, parent, option, index):
        pass
        #self.combo = IconComboBox(self.imageLocation, parent)
        #return self.combo

    def setEditorData(self, editor, index):
        value = str(index.model().data(index, Qt.EditRole))
        editor.setCurrentIndex(editor.findText(value))

    def setModelData(self, editor, model, index):
        if editor.currentIndex() >= 0:
            realidx = editor.model().index(editor.currentIndex(), 0)
            value = editor.model().data(realidx)
            model.setData(index, value, Qt.EditRole)

    def CreateImage(self):
        self.SizeX = 600
        self.SizeY = 256
        self.color1 = QColor()
        self.color2 = QColor()
        self.PixelMap = QImage(self.SizeX, self.SizeY, QImage.Format_RGB32)
        self.MaskImage = QImage(self.SizeX, self.SizeY, QImage.Format_RGB32)

        #self.NumpyImage = np.empty((self.SizeX,self.SizeY),np.uint32)

        self.NumpyImage = np.zeros((self.SizeY, self.SizeX, 3), dtype=np.uint8)
        #Color One
        self.H1= 23 #random.randint(1,256)
        self.S1 = 123 # random.randint(1,256)
        self.V1 = 152 #random.randint(1,256)

        #self.PixelMap.fill(qRgb(self.color1.red(),self.color1.blue(),self.color1.green()))

        #Color 2
        self.H2 = 123 #random.randint(1,256)
        self.S2 = 221 #random.randint(1,256)
        self.V2 = 15 #random.randint(1,256)

        #Background Color
        self.NumpyImage[0:self.SizeY, 0:self.SizeX,:] = 255 #self.color1

        #Ten Minute Dividers
        for ColumnColor in range(6):
            self.NumpyImage[0:self.SizeY, 100*ColumnColor ,:] = 0 #self.color1

        VerticalBorder = 50

        for ColumnColor in range(self.SizeX):
            colorvalue = random.randint(0,1)

            if colorvalue == 1:
                self.NumpyImage[VerticalBorder:self.SizeY-VerticalBorder, ColumnColor,0] = self.H1 #self.color1
                self.NumpyImage[VerticalBorder:self.SizeY-VerticalBorder, ColumnColor,1] = self.S1 #self.color1
                self.NumpyImage[VerticalBorder:self.SizeY-VerticalBorder, ColumnColor,2] = self.V1 #self.color1
            else:
                self.NumpyImage[VerticalBorder:self.SizeY-VerticalBorder, ColumnColor,0] = self.H2 #self.color1
                self.NumpyImage[VerticalBorder:self.SizeY-VerticalBorder, ColumnColor,1] = self.S2 #self.color1
                self.NumpyImage[VerticalBorder:self.SizeY-VerticalBorder, ColumnColor,2] = self.V2 #self.color1

        self.Image = array2qimage(self.NumpyImage, normalize = False) # create QImage from ndarray

        self.OutputFilename = "D:\Dropbox (Personal)\David Lario - Office\Development\Python\Projects\Timetrack\TimeTracker\Timetracker\TimeTrackIcon.jpg"
        success = self.Image.save(self.OutputFilename) # use Qt's image IO functions for saving PNG/JPG/..
        #self.CreateVerticalLines()

