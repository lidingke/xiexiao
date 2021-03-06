from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QSizePolicy
from PyQt5.QtCore import pyqtSignal
from model.database import DataHand
import time
import pdb
# from toolkit import WRpickle

class HistoryList(QListWidget):
    """docstring for HistoryList"""
    itemSelectedEmit = pyqtSignal(object)

    def __init__(self,):
        super(HistoryList, self).__init__()
        self.datahand = DataHand()
        self.nowtable = 0
        self.itemSelectionChanged.connect(self.itemSelect)
        self.table = []
        self.setCurrentRow(1)
        self.getTable()
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.updateGeometry()


    def getTable(self):

        count = self.count()
        print('count', count)
        table = self.datahand.getTable()
        if count == 0:
            for  x in  table[::-1]:
                item = self._createItem(x)
                self.addItem(item)
        else:
            if len(table) > count:
                item = table[-1]
                item = self._createItem(item)
                self.insertItem(0,item)

        print('count', count, len(table))
        self.nowtable = table[-1][0]
        self.table = table
        # print(self.nowtable,type(self.nowtable))

    def _createItem(self, item):
        xsplit = item[0].split('US')
        timetick = xsplit[0][2:]
        username = xsplit[1]
        timeShow = time.strftime('%Y:%m:%d||%H:%M:%S',
                                 time.localtime(int(timetick)))
        itemGet = QListWidgetItem('时间:{}用户:{}'.format(timeShow, username))
        itemGet.tableName = item[0]

        return itemGet

    def getTableData(self):
        return self.datahand.getTableData(self.nowtable)

    def itemSelect(self):
        self.itemText = self.currentItem().tableName
        self.itemIndex = self.table[-1-int(self.currentRow())][0]
        print(self.itemText,self.itemIndex)
        self.itemSelectedEmit.emit(self.itemIndex)


if __name__ == '__main__':

    import sys

    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    ad = HistoryList()
    ad.show()
    ad.getTable()
    data = ad.getTableData()
    # print(len(data))

    sys.exit(app.exec_())
