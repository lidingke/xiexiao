#qt tool
from PyQt5.QtWidgets    import (QWidget, QVBoxLayout,
    QHBoxLayout, QPlainTextEdit, QApplication, QLineEdit, QSizePolicy)
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QRect
# from PyQt5.QtGui import
#python tool
import time
from queue              import Queue
import pdb

# from UI.portGBUI import Ui_GroupBox as PortGBUI
# from UI.pumpUI import Ui_GroupBox as PumpUI
# from UI.powerUI import Ui_Form as PowerUI
# from portGBUI import Ui_GroupBox as PortGBUI
from UI.mainUI import Ui_Form as TabBoxUI
from .canvas import TwoLinePlot
from .powershow import PowerShow
from .user import UserView
from frame.lastlog import LastLog
# from view.powerrecord import PowerRecord
# from view.user import User
# from model.lastlog import LastLog
import threading


class View(QWidget):
    """build from photodarker view"""
    startPumpModel = pyqtSignal(object)
    setBaundratePortSignal = pyqtSignal(object,object)
    emitTabBoxStatus = pyqtSignal(object, object)
    # setSignal = pyqtSignal(object)


    def __init__(self,):
        super(View, self).__init__()
        QWidget.__init__(self)
        self.__initUI()
        self.queue      = Queue()
        self._setLastLog()


    def __initUI(self):
        self.tabBoxUI = TabBoxUI()
        self.tabBoxUI.setupUi(self)
        self.__initTabBox()
        self.__initUserUI()
        self.__initPort()
        self.__initMatplotUI()
        self.__initLog()
        self.__initPowerShow()
        self._initTabStateChange()
        # temp disable tabbox


    def __initTabBox(self):
        # self.tabBoxUI.setGeometry(QRect(0, 0, 700, 600))
        # self.tabBoxUI.tabBox.setTabEnabled(3, False)
        # self.tabBoxUI.helpTab.hide()
        print(self.tabBoxUI.verticalLayoutWidget)
        bugkey = []
        for k,v in self.tabBoxUI.__dict__.items():
            if isinstance(v, QWidget):
                if type(v) != QWidget:
                    bugkey.append("QWidget#"+str(k)+', ')
        # pdb.set_trace()
        print(''.join(bugkey))
        # self.tabBoxUI.tabBox.setTabEnabled(1, False)
        # self.tabBoxUI.tabBox.setTabEnabled(2, False)
        # self.tabBoxUI.tabBox.setTabEnabled(3, False)


    def __initUserUI(self):
        self.myUserUI = MyUserUI(self.tabBoxUI)


    def __initPort(self):
        menuItem = ['300 baud','1200 baud',
            '2400 baud','4800 baud','9600 baud',
            '19200 baud','38400 baud','57600 baud',
            '115200 baud','230400 baud','250000 baud']
        self.tabBoxUI.baundrate.addItems(menuItem)
        portItem = ['com1','com2','com3','com4',
            'com5','com6','com7','com8','com9',
            'com10','com11','com12','com13',
            'com14','com15','com16','com17',
            'com18','com19','com20']
        self.tabBoxUI.port.addItems(portItem)
        self.tabBoxUI.baundrate.currentIndexChanged.connect(self.emitBaundratePort)
        self.tabBoxUI.port.currentIndexChanged.connect(self.emitBaundratePort)
        def openEvent():
            self.tabBoxUI.closePort.setEnabled(True)
            self.tabBoxUI.openPort.setEnabled(False)
            self.tabBoxUI.tabBox.setTabEnabled(2, True)
        self.tabBoxUI.openPort.clicked.connect(openEvent)
        def closeEvent():
            self.tabBoxUI.closePort.setEnabled(False)
            self.tabBoxUI.openPort.setEnabled(True)
            self.tabBoxUI.tabBox.setTabEnabled(2, False)
        self.tabBoxUI.closePort.clicked.connect(closeEvent)

    def __initMatplotUI(self):
        # matplot = self.tabBoxUI.
        matplot = QWidget()
        self.painter = TwoLinePlot(matplot, width=5, height=4, dpi=100)
        self.tabBoxUI.mainLayout.addWidget(self.painter)
        # self.painter.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        # self.painter.updateGeometry()
        # self.tabBoxUI.mainLayout.replaceWidget(matplot,self.painter)

    def __initPowerShow(self):
        self.powerShow1 = PowerShow()
        self.powerShow2 = PowerShow()
        self.tabBoxUI.tabsides.addWidget(self.powerShow1)
        self.tabBoxUI.tabsides.addWidget(self.powerShow2)
        # self.tabBoxUI.cmdLayout.addWidget(QPlainTextEdit())

    def __initLog(self):
        self.powerLog = PowerLog(self.tabBoxUI)
        self.powerLog.getNowFig(self.painter)
        # self.powerLog.timeStateSignal.connect(self.painter.getLogTimeState)
        # self.powerLog.logStateSignal.connect(self.painter.getStartLog)
        self.powerLog.plotlist.connect(self.painter.XYaxit)

    def _setLastLog(self):
        self.lastLog = LastLog()
        print('lastlog dict:', self.lastLog)
        userName = self.lastLog.get('username','')
        password = self.lastLog.get('password','')
        baudIndex = self.lastLog.get('baud', 4)
        portIndex = self.lastLog.get('port', 0)

        self.tabBoxUI.userName.setText(userName)
        self.tabBoxUI.passwordIput.setText(password)
        self.tabBoxUI.baundrate.setCurrentIndex(baudIndex)
        self.tabBoxUI.port.setCurrentIndex(portIndex)

    def lastLogSave(self):
        self.lastLog['username'] = self.tabBoxUI.userName.text()
        self.lastLog['password'] = self.tabBoxUI.passwordIput.text()
        self.lastLog['baud'] = self.tabBoxUI.baundrate.currentIndex()
        self.lastLog['port'] = self.tabBoxUI.port.currentIndex()
        self.lastLog.saveLast()

    # def __setUser(self,value):
    #     pass

    def set_queue(self, queue):
        self.queue = queue

    def set_end_cmd(self, end_cmd):
        self.end_cmd = end_cmd

    def setPowerShowDict(self,dct1, dct2):
        """
        singnal from model.updatePowerShow
        """
        self.powerShow1.powerList = dct1
        self.powerShow1.updateFigure()
        self.powerShow2.powerList = dct2
        self.powerShow2.updateFigure()

    def updataFigure(self,newtime,power1, power2):
        # self.setCurrentValue(currentValue, timeValue)
        self.painter.XYaxit(newtime, power1, power2)


    def emitBaundratePort(self):
        bp = self.getBaundratePort()
        self.setBaundratePortSignal.emit(bp[0],bp[1])

    def getBaundratePort(self):
        port = self.tabBoxUI.port.currentText()
        baundrate = self.tabBoxUI.baundrate.currentText()[:-5]
        baundrate = int(baundrate)
        return (port,baundrate)

    # def setPort(self):
    #     self.setPortSignal.emit()

    def update_gui(self):
        # self.process_incoming()
        self.update()

    # def set_end_cmd(self,end_cmd):
    def closeEvent(self, event):
        self.lastLogSave()
        print('last log ',self.lastLog)
        QWidget.closeEvent(self, event)

    def _initTabStateChange(self):
        def openport():
            self._tabBoxStateManager('openPort',{})
            self.tabBoxUI.openPlatform.setEnabled(False)
            self.tabBoxUI.closePlatform.setEnabled(True)
        self.tabBoxUI.openPlatform.clicked.connect(openport)

        def closeport():
            self._tabBoxStateManager('closePort', {})
            self.tabBoxUI.openPlatform.setEnabled(True)
            self.tabBoxUI.closePlatform.setEnabled(False)
        self.tabBoxUI.closePlatform.clicked.connect(closeport)
        getCurrentIndex = self.tabBoxUI.tabBox.currentIndex

        def startlog():
            print ('get in startlog', getCurrentIndex())
            self._tabBoxStateManager('startLog', {'currentIndex':getCurrentIndex()})
        vchangebox = ValueChanged(getCurrentIndex)
        vchangebox.changed.connect(startlog)
        # self.tabBoxUI.tabBox.isTabChanged.connect(startlog)
    #

    def _tabBoxStateManager(self, state, para):
        if state == 'openPort':
            self.emitTabBoxStatus.emit(state, para)
        elif state == 'closePort':
            self.emitTabBoxStatus.emit(state, para)
        elif state == 'startLog':
            self.emitTabBoxStatus.emit(state, para)


class ValueChanged(QObject):
    changed = pyqtSignal()
    def __init__(self, getfun):
        # super(valueChanged, self).__init__()
        QObject.__init__(self)
        self.value = False
        self.getfun = getfun
        threading.Thread(target= self._monitor, daemon = True).start()

    def _monitor(self):
        while True:
            getfunvalue = self.getfun()
            if self.value != getfunvalue:
                self.value = getfunvalue
                self.changed.emit()
            time.sleep(0.3)


class MyUserUI(UserView,QObject):
    """docstring for myUserUI"""
    def __init__(self,father):
        self.father = father
        super(MyUserUI, self).__init__()
        QObject.__init__(self)

    def UI_init(self):
        self.passwordIput = self.father.passwordIput
        self.login = self.father.login
        self.register = self.father.userRegister
        self.nameIput = self.father.userName
        self.passwordIput.setEchoMode(QLineEdit.Password)
        self.login.status = 'login'
        self.login.clicked.connect(self.loginfun)
        self.register.clicked.connect(self.registerfun)

from view.powerrecord import PowerRecord
class PowerLog(PowerRecord, QObject):
    """docstring for PowerLog"""
    def __init__(self, father):
        self.father = father
        super (PowerLog, self).__init__()
        # self.arg = arg


    def _setupUi(self):
        self.logButton = self.father.logButton
        self.stepEdit = self.father.stepEdit
        self.printButton = self.father.printButton
        self.timeEdit = self.father.timeEdit
        self.gridLayout_2 = self.father.logGridLayout
        self.gridLayout = self.father.historyGridLayout
        self.ticker = self.father.ticker
        self.historyEdit = self.father.historyEdit
        # self.ticker = self
        # pass



if __name__ == '__main__':
    app         = QApplication(sys.argv)
    gui         = View()

    gui.show()

    sys.exit(app.exec_())
