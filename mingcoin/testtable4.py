from PyQt4.QtGui import * 
from PyQt4.QtCore import * 
import sys

lista = ['aa', 'ab', 'ac']
listb = ['ba', 'bb', 'bc']
listc = ['ca', 'cb', 'cc']
mystruct = {'A':lista, 'B':listb, 'C':listc}

class MyTable(QTableWidget):
    def __init__(self, thestruct, *args):
        QTableWidget.__init__(self, *args)
        self.data = thestruct
        self.setmydata()
        self.setHorizontalHeaderLabels(QString("H1;H2;").split(";"))
        self.setVerticalHeaderLabels(QString("V1;V2").split(";"))
    def setmydata(self):
        n = 0
        for key in self.data:
            m = 0
            for item in self.data[key]:
                newitem = QTableWidgetItem(item)
                self.setItem(m, n, newitem)
                m += 1
            n += 1

def main(args):
    app = QApplication(args)
    table = MyTable(mystruct, 5, 3)
    table.show()
    sys.exit(app.exec_())
    
if __name__=="__main__":
    main(sys.argv)