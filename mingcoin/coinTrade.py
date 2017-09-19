# -*- coding: utf-8 -*-

# slider.py

import sys
from coinApi import *

# from PyQt4 import QtGui
# from PyQt4 import QtCore
from PyQt4.QtGui import * 
from PyQt4.QtCore import * 


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.table1 = ExampleTable()
        self.layout1 = ExampleLayout()
        #self.form_widget = FormWidget(self)
        _widget = QWidget()
        _layout = QVBoxLayout(_widget)
        _layout.addWidget(self.table1)
        _layout.addChildWidget(self.layout1)
        self.setCentralWidget(_widget)

# class ExampleTable(QtGui.QWidget):
class ExampleTable(QTableWidget):

    def __init__(self):
        super(ExampleTable, self).__init__()

        self.initUI()

    def cellClick(row,col):
        print "Click on " + str(row) + " " + str(col)
    
    def initUI(self):  
        # table 	= QtGui.QTableWidget()
        self.tableItem 	= QTableWidgetItem()
        self.setWindowTitle("QTableWidget Example @pythonspot.com")
        self.resize(400, 250)
        self.setRowCount(4)
        self.setColumnCount(2)
    
        # set label
        self.setHorizontalHeaderLabels(QString("H1;H2;").split(";"))
        self.setVerticalHeaderLabels(QString("V1;V2;V3;V4").split(";"))
    
        # set data
        self.setItem(0,0, QTableWidgetItem("Item (1,1)"))
        self.setItem(0,1, QTableWidgetItem("Item (1,2)"))
        self.setItem(1,0, QTableWidgetItem("Item (2,1)"))
        self.setItem(1,1, QTableWidgetItem("Item (2,2)"))
        self.setItem(2,0, QTableWidgetItem("Item (3,1)"))
        self.setItem(2,1, QTableWidgetItem("Item (3,2)"))
        self.setItem(3,0, QTableWidgetItem("Item (4,1)"))
        self.setItem(3,1, QTableWidgetItem("Item (4,2)"))
    
        # tooltip text
        self.horizontalHeaderItem(0).setToolTip("Column 1 ")
        self.horizontalHeaderItem(1).setToolTip("Column 2 ")  
    
        # on click function
        #table.cellClicked.connect(cellClick)
        # show table
        #table.show()

class ExampleLayout(QWidget):

    def __init__(self):
        super(ExampleLayout, self).__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle(u'主控台')

        names = [u'行情', '交易', '', 'Close', '7', '8', '9', '/',
            '4', '5', '6', '*', '1', '2', '3', '-',
            '0', '.', '=', '+']

        grid = QGridLayout()

        j = 0
        pos = [(0, 0), (0, 1), (0, 2), (0, 3),
                (1, 0), (1, 1), (1, 2), (1, 3),
                (2, 0), (2, 1), (2, 2), (2, 3),
                (3, 0), (3, 1), (3, 2), (3, 3 ),
                (4, 0), (4, 1), (4, 2), (4, 3)]

        for i in names:
            button = QPushButton(i)
            if j == 2:
                grid.addWidget(QLabel(''), 0, 2)
            else: grid.addWidget(button, pos[j][0], pos[j][1])
            j = j + 1

        self.setLayout(grid)


class ExampleSlider(QWidget):

    def __init__(self):
        super(ExampleSlider, self).__init__()

        self.initUI()

    def initUI(self):

        slider = QSlider(Qt.Horizontal, self)
        slider.setFocusPolicy(Qt.NoFocus)
        slider.setGeometry(30, 40, 100, 30)
        self.connect(slider, SIGNAL('valueChanged(int)'),
            self.changeValue)

        self.label = QLabel(self)
        self.label.setPixmap(QPixmap('mute.png'))
        self.label.setGeometry(160, 40, 80, 30)

        self.setWindowTitle('Slider')
        self.setGeometry(300, 300, 250, 150)


    def changeValue(self, value):

        if value == 0:
            self.label.setPixmap(QPixmap('mute.png'))
        elif value > 0 and value <= 30:
            self.label.setPixmap(QPixmap('min.png'))
        elif value > 30 and value < 80:
            self.label.setPixmap(QPixmap('med.png'))
        else:
            self.label.setPixmap(QPixmap('max.png'))

class ExampleBox(QWidget):

    def __init__(self):
        super(ExampleBox, self).__init__()

        self.initUI()

    def initUI(self):
        okButton = QPushButton("OK")
        cancelButton = QPushButton("Cancel")

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(okButton)
        hbox.addWidget(cancelButton)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.setWindowTitle('box layout')
        self.resize(300, 150)



if __name__ == '__main__':

    app = QApplication(sys.argv)
    win = MainWindow()
    # exlayout = ExampleLayout()
    # exslider = ExampleSlider()
    # extable = ExampleTable()
    # exlayout.show()
    # exslider.show()
    # extable.show()
    win.show()
    app.exec_()