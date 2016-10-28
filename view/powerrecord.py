# PyQt lib
from PyQt5.QtCore import (pyqtSignal, Qt)
from PyQt5.QtWidgets import (QWidget, QMessageBox, QSizePolicy)

#py lib
import time
import pickle
import queue
import numpy
# view
from view.pdfcreater import PdfCreater
from view.reportDialog import ReportDialog
from view.ticker import Ticker
from view.historylist import HistoryList
#UI
from UI.recordUI import Ui_Form as RecodUI
#model
from frame.singleton import PickContext
from model.database import DataHand


class PowerRecord(QWidget,RecodUI):
    """docstring for PowerRecord"""

    emitBeginTime = pyqtSignal(object, object)
    emitSqlTableName = pyqtSignal(object)
    emitLogStartOrStop = pyqtSignal(object)
    # timeStateSignal = pyqtSignal(object)
    # logStateSignal = pyqtSignal(object)
    plotlist = pyqtSignal(object,object,object)
    # plotlistbegin = pyqtSignal(object)

    def __init__(self):
        super(PowerRecord, self).__init__()
        self.pickContext = PickContext()
        self.datahand = DataHand()
        # self.startTime = 0
        self.stopTime = time.time()
        self.userID = ''
        self.powerData = queue.Queue()
        self.pick = list()
        self.itemShowNum = 4
        self.itemChangeStatus = False
        self.timeStepPause = False
        # self.pdfItem = dict()
        self.figGet = None
        self.timebegin = True
        # self.loadFile()
        self.UI_init()


    def _setupUi(self):
        self.setupUi(self)

    def UI_init(self):
        self._setupUi()
        self.seButton = self.logButton
        self.seButton.buttonState = 'begin'
        self.seButton.clicked.connect(self.logSignalManager)
        # self.timeEdit = self.timeEdit
        self.timeEdit.setDisplayFormat(' s : hh : mm')
        print('time edit',self.timeEdit)
        # self.timeEdit.setDate(QDate(2000,10,10))
        # print(self.timeEdit.text())
        self.ticker.hide()
        self.ticker = Ticker()
        self.gridLayout.addWidget(self.ticker, 3, 1, 1, 1)
        # self.formLayout.setWidget(3, QFormLayout.FieldRole, self.ticker)
        self.ticker.start()
        self.ticker.timeOut.connect(self.tickerTimeOut)
        # self.ticker.setNumDigits(10)
        # self.ticker.display('00:00:00')

        self.historyEdit.hide()
        self.historyEdit = HistoryList()
        print('hist',self.historyEdit)
        # self.historyEdit.parent = self
        self.gridLayout_2.addWidget(self.historyEdit, 1, 0, 1, 2)
        self.historyEdit.itemSelectedEmit.connect(self.itemSelectionChanged)
        self.historyEdit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.printButton.clicked.connect(self.printReport)
        # self.historyEdit.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # self.historyEdit.updateGeometry()


    def itemSelectionChanged(self,item):
        #todo: change pickcontext to double
        print('getitem',item)
        #get nowtable
        self.tableName = item
        self.emitSqlTableName.emit(self.tableName)
        temp = item.split('US')
        self.userID = temp[1]
        self.timeTick = temp[2:]
        # self.NowContextGet()
        #get last log
        self.pickContext = PickContext()
        #get username
        self.pickContext['worker'] = self.userID
        #get plot from db
        plotdata = self.datahand.getTableData(self.tableName)
        time_ = []
        power1 = []
        power2 = []
        for x in plotdata:
            time_.append(x[0])
            power1.append(x[1])
            power2.append(x[2])
        self.plotlist.emit(time_, power1, power2)
        power = power1
        #get calc report
        if time_:
            self.pickContext['timelong'] = str(int(time_[-1]-time_[0]))+'秒'
            self.pickContext['maxsignalpower'] = self.__Power2str(max(power))
            self.pickContext['minsingalpower'] = self.__Power2str(min(power))
            self.pickContext['averagesingalepower'] = self.__Power2str(numpy.mean(power))
            self.pickContext['powerstable'] = self.__Power2str(numpy.std(power))
        else:
            self.pickContext['timelong'] = '0'
            self.pickContext['maxsignalpower'] = '0'
            self.pickContext['minsingalpower'] = '0'
            self.pickContext['averagesingalepower'] = '0'
            self.pickContext['powerstable'] = '0'
        print('PowerRecord change')
        self.pickContext.save_pick_file()

    def printReport(self):
        # self.getDbdata()
        if self.figGet:
            self.figGet.savePlotFig()
        rep = ReportDialog(self)
        # print('rep',rep)
        rep.exec_()
        if rep.saveOrcancel == 'save':
            print('pickContext',self.pickContext.pickContext)
            printer = PdfCreater(self,)
            self.emitSqlTableName.connect(printer.getDBData)
            printer.saveToFile()
        # printer.savePdf()

        # if self.itemChangeStatus is False:
        #     self.itemText = self.historyEdit.item(0).text()
        # print('print:',self.itemText)
        # self.pdfItem['']

    def getNowFig(self,fig):
        self.figGet = fig


    # def NowContextGet(self):


    # # def plotTable():
    #     pass


    def logSignalManager(self):
        # self.ticker.run()
        if self.seButton.buttonState == 'begin':
            self.timeLong = self.timeEdit2time()
            self.timeStep = int(self.stepEdit.text()[:-1])
            if self.timeLong < self.timeStep:
                QMessageBox.information(self, "设置错误","记录时长要比记录步长大")
                return
            # else:
            #记录起始时间
            self.beginTime = time.time()
            print('stepEdit',self.stepEdit.text()[:-1],'beginTime:',self.beginTime)
            # emit to model.setStartTime
            self.emitBeginTime.emit(self.beginTime, self.timeStep)
            self.emitLogStartOrStop.emit(True)
            # self.timeStateSignal.emit(self.timeLong)
            self.ticker.startTick(self.timeLong)
            # self.logStateSignal.emit(True)
            self.seButton.setText('停止')
            self.seButton.buttonState = 'stop'
        elif self.seButton.buttonState == 'stop':
            self.ticker.stopTick()
            self.seButton.setText('开始')
            self.seButton.buttonState = 'begin'
            self.emitLogStartOrStop.emit(False)
            self.historyEdit.getTable()


    def tickerTimeOut(self):
        print('time out')
        self.seButton.setText('开始')
        self.seButton.buttonState = 'begin'
        self.emitLogStartOrStop.emit(False)
        self.historyEdit.getTable()


    def timeEdit2time(self):
        timeStr = self.timeEdit.text()
        timeSplit = timeStr.split(':')
        date = int(timeSplit[0].strip())
        hour = int(timeSplit[1].strip())
        minute = int(timeSplit[2].strip())
        return ((date*24+hour)*60+minute)*60

    def update_GUI(self):
        self.update()

###
# interface
###

    def getUserID(self):
        return self.userID

    def setUserID(self,userid):
        self.userID = userid

    def getPowerData(self):
        return self.powerData

    def setPowerData(self,data):
        self.powerData.put(data)



    def getDbdata(self):
        if self.itemChangeStatus is False:
            self.itemText = self.historyEdit.item(0).text()
            self.itemNum = 0
            pickget = self.pick[-self.itemNum-1]
            self.startTimetic = pickget.get('begin')
            self.printUserID = pickget.get('userID')
            print('num,pick:',self.itemNum, self.startTimetic)
            print('print:',self.itemText)
        localTime = self.startTimetic
        username = self.userID
        localTime = str(int(localTime))
        tableName='TM'+localTime+'US'+username
        self.emitSqlTableName.emit(tableName)

    def timerSave(self):
        beginTime =self.beginTime
        continueTime = self.editTime
        self.pick.append({'begin':beginTime,
            'continue':continueTime,'userID':self.userID})
        self.saveFile()
        self.loadFile()
        self.plantlist()

        self.stopTime = time.time()
        self.seButton.setEnabled(True)
        self.emitLogStartOrStop.emit(False)
        # self.seButton.setText('start')
        # self.timebegin = False

    def loadFile(self):
        try:
            with open('data\\usertask.pickle','rb') as f:
                self.pick = pickle.load(f)
                f.close()
        except FileNotFoundError:
            newfile = open('data\\usertask.pickle','wb')
            self.pick = list()
            pickle.dump(self.pick,newfile)
            newfile.close()
            # self.loadFile()
        except EOFError :
            pass

        except Exception as e:
            raise e

    def saveFile(self):
        try:
            with open('data\\usertask.pickle','wb') as f:
                pickle.dump(self.pick,f)
                f.close()
        except Exception as e:
            raise e

    def plantlist(self):
        if len(self.pick) < self.itemShowNum:
            textlist = self.pick
        else:
            textlist = self.pick[-self.itemShowNum:]
        for i,x in enumerate(textlist):
            if x.get('start',False) is not False:
                pass
                starttime = time.strftime('%H:%M:%S',time.localtime(x.get('start')))
                stoptime = time.strftime('%H:%M:%S',time.localtime(x.get('stop')))
                textstr = 'start:'+starttime+', stop:'+stoptime+', user:'+x.get('userID')
            elif x.get('begin',False) is not False:
                begin = time.strftime('%H:%M:%S',time.localtime(x.get('begin')))
                con = x.get('continue').toString()
                textstr = 'begin:' + begin + ', cont:' + con + ', user:'+x.get('userID')
            if i < self.itemShowNum:
                item = self.historyEdit.item(self.itemShowNum-i-1)
                item.setText(textstr)

    def __Power2str(self,data):
        if data > 0.1:
            return str(round(data,2))+'W'
        else:
            return str(round(data*1000,2)) + 'mW'


###
#emit
###
    # def emitBeginTime(self):
    #     self.beginTime.emit(self.beginTime)


if __name__ == '__main__':
    import sys

    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    addressBook = PowerRecord()
    addressBook.show()

    sys.exit(app.exec_())
