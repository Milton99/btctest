# -*- coding: utf-8 -*-

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from coinApi import *
#import coinApi




class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        # QMainWindow.__init__(self,parent)

        self.initUI()

    def initUI(self):  

        self.lbl_title = QLabel(u'主控台')
        self.lbl_spacer = QLabel(u'1')

        self.mainTable = MainTable()
        self.btn_cancel_buy = QPushButton(u'撤买单')
        self.btn_cancel_sell = QPushButton(u'撤卖单')
        self.btn_cancel_all = QPushButton(u'全部撤销')

        self.btn_buy = QPushButton(u'建买单')
        self.btn_sell = QPushButton(u'建卖单')

        self.btn_buy_market = QPushButton(u'即刻买')
        self.btn_sell_market = QPushButton(u'即刻卖')

        self.txt_buy_price = QLineEdit()
        self.txt_buy_qty = QLineEdit()
        self.txt_sell_price = QLineEdit()
        self.txt_sell_qty = QLineEdit()

        _widget = QWidget()
        grid = QGridLayout(_widget)

        OBR=13
        OBC=1
        grid.addWidget(self.lbl_title, 0, 3, 1, 3)
        grid.addWidget(self.mainTable, 2, 1, 6, 9)
        grid.addWidget(self.btn_cancel_buy, 4, 11, 1, 2)
        grid.addWidget(self.btn_cancel_sell, 5, 11, 1, 2)
        grid.addWidget(self.btn_cancel_all, 6, 11, 1, 2)
        grid.addWidget(self.btn_buy, OBR, 1, 1, 1)
        grid.addWidget(self.btn_sell, OBR+2, 1, 1, 1)
        grid.addWidget(self.txt_buy_price, OBR, 3, 1, 2)
        grid.addWidget(self.txt_buy_qty, OBR, 6, 1, 2)
        grid.addWidget(self.txt_sell_price, OBR+2, 3, 1, 2)
        grid.addWidget(self.txt_sell_qty, OBR+2, 6, 1, 2)
        grid.addWidget(self.btn_buy_market,OBR, 9, 1, 2)
        grid.addWidget(self.btn_sell_market,OBR+2, 9, 1, 2)
        grid.addWidget(self.lbl_spacer, 9, 1, 2, 1)

        grid.setSpacing(10)
        self.setLayout(grid)
        self.setCentralWidget(_widget)
        self.resize(900,450)

        #self.connect(self.btn_buy,  SIGNAL('clicked()'), self, SLOT('updater()'))
        self.connect(self.btn_buy,SIGNAL('clicked()'), self.lbl_title, SLOT('updater()'))
          #self.connect(self.btn_buy,SIGNAL('clicked()'), self.lbl_title, SLOT('updater()'))
        
    def showDialog(self):
        text, ok=QInputDialog.getText(self,'Input Dialog', 'Enter yourname:')
        if ok:
            self.label.setText(unicode(text))

    def updater(self):
        # 查询当前行情
        m_btc = MarketCondition(market = "btctrade", coin = "btc", logging = False).get_ticker()
        m_eth = MarketCondition(market = "btctrade", coin = "eth", logging = False).get_ticker()
        m_ltc = MarketCondition(market = "btctrade", coin = "ltc", logging = False).get_ticker()
        m_doge = MarketCondition(market = "btctrade", coin = "doge", logging = False).get_ticker()
        m_ybc = MarketCondition(market = "btctrade", coin = "ybc", logging = False).get_ticker()
        # self.mainTable.setItem(0,0, QTableWidgetItem("%.2f" %m_btc['last'] ))
        self.setTitle(self.tr("AClient"))

        # 查询账户资产信息
        dealer_balance = Dealer(market = "btctrade", coin = "btc",  logging = False).get_balance()
        dealer_balance = {key: float(value) for (key,value) in dealer_balance.items()} 

        #折算人民币价值
        cny_balance={}
        cny_balance['cny'] = (dealer_balance['cny_balance'] + dealer_balance['cny_reserved']) 
        cny_balance['btc'] = (dealer_balance['btc_balance'] + dealer_balance['btc_reserved']) * m_btc['last']
        cny_balance['eth'] = (dealer_balance['eth_balance'] + dealer_balance['eth_reserved']) * m_eth['last']
        cny_balance['ltc'] = (dealer_balance['ltc_balance'] + dealer_balance['ltc_reserved']) * m_ltc['last']
        cny_balance['doge'] = (dealer_balance['doge_balance'] + dealer_balance['doge_reserved']) * m_doge['last']
        cny_balance['ybc'] = (dealer_balance['ybc_balance'] + dealer_balance['ybc_reserved']) * m_ybc['last']
        value_total = sum(cny_balance.values())

        for k,v in cny_balance.items():
            print "the rmb value of " + k + " is： %f" %v

        print "财产折合人民币：%.2f" %value_total
        print "财产折合比特币: %f" %(value_total/m_btc['last'])
        rate=6.87
        print "比特币现行价: %.2f" %m_btc['last'] + " 元 or " + ("%.2f" %(m_btc['last']/rate)) + " 美金"
        

class MainTable(QTableWidget):

    def __init__(self):
        super(MainTable, self).__init__()

        self.initUI()

    def cellClick(row,col):
        print "Click on " + str(row) + " " + str(col)
    
    def initUI(self):  
        # table 	= QtGui.QTableWidget()
        self.tableItem 	= QTableWidgetItem()
        # self.setWindowTitle("QTableWidget Example @pythonspot.com")
        self.resize(100, 100)
        self.setRowCount(6)
        self.setColumnCount(6)
    
        # set label
        self.setHorizontalHeaderLabels(QString("Btc;Eth;Ltc;Goge;Ybc;Cny").split(";"))
        self.setVerticalHeaderLabels(QString(u"市场买价;市场卖价;最后价格;结存额度;冻结额度;可用额度").split(";"))

        # set data
        self.setItem(0,0, QTableWidgetItem("xxx" ))
        self.setItem(0,1, QTableWidgetItem("Item (1,2)"))
        self.setItem(1,0, QTableWidgetItem("Item (2,1)"))
        self.setItem(1,1, QTableWidgetItem("Item (2,2)"))
        self.setItem(2,0, QTableWidgetItem("Item (3,1)"))
        self.setItem(2,1, QTableWidgetItem("Item (3,2)"))
        self.setItem(3,0, QTableWidgetItem("Item (4,1)"))
        self.setItem(3,1, QTableWidgetItem("Item (4,2)"))
    
        # tooltip text
        # self.horizontalHeaderItem(0).setToolTip("Column 1 ")
        # self.horizontalHeaderItem(1).setToolTip("Column 2 ")  


def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec_()

if __name__ == '__main__':
    sys.exit(main()) 