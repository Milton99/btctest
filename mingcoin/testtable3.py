import sys
from PyQt4 import QtGui
class GridLayout(QtGui.QWidget):
    def __init__(self,parent=None):
 
        QtGui.QWidget.__init__(self)

        self.setWindowTitle('gridlayout')

        title =QtGui.QLabel('Title')
        authot=QtGui.QLabel('Author')
        review=QtGui.QLabel('Review')

        titleEdit =QtGui.QLineEdit()
        authorEdit=QtGui.QLineEdit()
        reviewEdit =QtGui.QLineEdit()

        title2 =QtGui.QLabel('Title')
        authot2=QtGui.QLabel('Author')
        review2=QtGui.QLabel('Review')

        titleEdit2 =QtGui.QLineEdit()
        authorEdit2=QtGui.QLineEdit()
        reviewEdit2 =QtGui.QLineEdit()

        grid=QtGui.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(title,1,1,2,4)
        grid.addWidget(titleEdit,1,1)

        grid.addWidget(title2,1,2)
        grid.addWidget(titleEdit2,1,3)
        grid.addWidget(authot2,1,4,2,1)
        grid.addWidget(authorEdit2,1,5)
        grid.addWidget(review2,1,6)
        grid.addWidget(reviewEdit2,1,7)

        grid.addWidget(authot,2,0)
        grid.addWidget(authorEdit,2,1)

        grid.addWidget(review,3,0,5,1)
        grid.addWidget(reviewEdit,3,1,5,5)

        self.setLayout(grid)
        self.resize(550,500)

app=QtGui.QApplication(sys.argv)
qb=GridLayout()
qb.show()
sys.exit(app.exec_())