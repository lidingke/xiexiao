from __future__ import division
from .modelcore import ModelCore
from PyQt5.QtCore import pyqtSignal, QObject
import threading
import time
from .database import DataHand

import pdb
from model.toolkit import HexSplit
import collections
# from dataSaveTick import DataSaveTick
import queue
import math
from model.loadjson import WriteReadJson

class ModelPump(ModelCore,QObject):
    """docstring for ModelPump"""
    emitPlot = pyqtSignal(object, object, object)
    beginPlot = pyqtSignal(object)
    updatePowerShow = pyqtSignal(object, object)
    updateLabelWarning = pyqtSignal(object, object)

    def __init__(self,):
        super(ModelPump, self).__init__()
        QObject.__init__(self)
        self.startRecord = False
        self.showPower1Data = {'logNumber': 0}
        self.showPower2Data = {'logNumber': 0}
        self.plotData = plotDataContainer()
        self.timebegin = False
        # self.tempdetector = TempDetector()
        self.logTimeStep = 1
        self.dataGetDict = {'dataGet': []}
        self.datasaveTick = DataSaveTick(self.logTimeStep, self.dataGetDict)
        self.datasaveTick.start()
        self.datasaveTick.resultEmite.connect(self.powerDataProcess)
        self.datahand = DataHand('data\\powerdata.db')
        self.datahand.username = self.username


    def setBaundratePort(self, port, baudrate):
        self.set_br(int(baudrate))
        self.set_port(port)
        self.reSetPort()
        msg = '串口号：{}，开关状态：{}'.format(self.ser.name,self.ser.is_open)
        self._viewWarning('port',msg)


    def closePort(self):
        super(ModelPump, self).closePort()
        msg = '串口号：{}，开关状态：{}'.format(self.ser.name,self.ser.is_open)
        self._viewWarning('port',msg)


    def openPlatform(self):
        self.plotData.setState('port')
        msg = self.msgDictHex['openpump']
        self.write(msg)


    def closePlatform(self):
        self.plotData.setState('port')
        msg = self.msgDictHex['closepump']
        self.write(msg)


    def setCurrent(self, current):
        current = int(current)
        msg = self.msgDictHex['setcurrent']
        msg = msg[:5] + current.to_bytes(2, 'big') + msg[7:]
        self.write(msg)

    def analysisbit(self):
        '''
                return without package
                input bit data analysis
        '''
        bitlist = list()
        while self.running:
            databit = self.readbit(self.ser)
            if databit == b'\xeb':
                # self.printShow(databit,'1')
                databit = self.readbit(self.ser)
                if databit == b'\x90':
                    while True:
                        databit = self.readbit(self.ser)
                        if databit == b'\x90':
                            databit = self.readbit(self.ser)
                            data = b''.join(bitlist)
                            self.printShow(data)
                            return data
                        bitlist.append(databit)
            elif databit == b'\x9A':
                tick = 1
                while True:
                    tick = tick + 1
                    databit = self.readbit(self.ser)
                    if databit == b'\xA9':
                        data = b''.join(bitlist)
                        print('get data',b'\x9A' + data + b'\xA9')
                        return b'\x9A' + data + b'\xA9'
                    bitlist.append(databit)


    def coreMsgProcess(self, data):
        if data[0:1] == b'\x9A':
            # print('POWER GET: ',data)
            self.dataGetDict['dataGet'].append([time.time(),data])


    def powerDataProcess(self, data1, data2):
        '''get power result and sent it to view
        emitPlot need connect to view.updataFigure
        updatePowerShow need connect to view.setPowerShowDict
        '''
        if not self.timebegin:
            self.timebegin = time.time()
        newtime = time.time()
        if self.startRecord == True:
            threading.Thread(target=self._save2sql, args=(data1, data2, '',), daemon=True).start()
        self.currentTime = newtime
        self.currentValue1 = data1
        self.currentValue2 = data2
        self.plotData.get(newtime, data1, data2)
        print ('get current ',data1, data2)
        if self.timebegin:
            emitresult = self.plotData.emit()

            self.emitPlot.emit(emitresult[0],emitresult[1],emitresult[2])
        self.showPower1Data = self._powerStatus(
            self.currentValue1, self.showPower1Data)
        self.showPower2Data = self._powerStatus(
            self.currentValue2, self.showPower2Data)
        self.updatePowerShow.emit(self.showPower1Data, self.showPower2Data)

    def _save2sql(self, power1 , power2, hexdata):
        startTime = str(int(self.timebegin))
        localTime = time.time()
        tableName = 'TM'+startTime+'US'+self.username
        try:
            self.datahand.save2Sql(tableName, localTime, power1, power2, hexdata)
        except Exception as e:
            raise e

    def _powerStatus(self, data, showPowerData):
        logNumber = showPowerData['logNumber'] + 1
        if logNumber < 2:
            # self.showPower1Data = [logNumber, data, data, 0, data, data]
            showPowerData = {
                'logNumber': logNumber,
                'currentPower': data,
                'averagePower': data,
                'variancePower': 0,
                'maxPower': data,
                'minPower': data}
        else:
            currentPower = showPowerData['currentPower']
            averagePower = showPowerData['averagePower']
            variancePower = showPowerData['variancePower']
            maxPower = showPowerData['maxPower']
            minPower = showPowerData['minPower']

            currentPower = data
            variancePower = \
                (logNumber - 2) * variancePower / (logNumber - 1) \
                + (data - averagePower) ** 2 / logNumber
            averagePower = averagePower + (data - averagePower) / logNumber

            if data > maxPower:
                maxPower = data
            if data < minPower:
                minPower = data

            showPowerData = {'logNumber': logNumber,
                                  'currentPower': currentPower,
                                  'averagePower': averagePower,
                                  'variancePower': variancePower,
                                  'maxPower': maxPower,
                                  'minPower': minPower}
        return showPowerData


    def setLogStartOrStop(self,isture):
        self.startRecord = isture
        self.plotData.setLogReStart(isture)
        # print('set startRecord:',self.startRecord)

    def createTable(self, tableName):
        data = self.datahand.getTableData(tableName)
        self.datahand.createPlot(data)

    #plot start status
    #todo: merge setBeginPlotTime and setStartTime
    def setBeginPlotTime(self):
        print('get ti0:', self.timebegin, 'init tabel username', self.username)
        self.datahand.initSqltabel(self.timebegin, self.username)
        self.beginPlot.emit(True)
        # self.plotData.setLogReStart(True)

    def setStartTime(self,begintime, steptime):
        self.timebegin = begintime
        self.datasaveTick.tick = steptime

    def plotStateGettedManager(self, state, para):
        if state == 'openPort':
            pass
        elif state == 'closePort':
            self.plotData.clearDynamicAxis()
        elif state == 'startLog':
            print ('get state',state, para)
            if para['currentIndex'] == 3:
                self.plotData.setState('log')
            else:
                self.plotData.setState('port')


    def _viewWarning(self, dirlabel, msg):
        print('isinstance', isinstance(dirlabel, str), isinstance(msg, str))
        if not isinstance(dirlabel, str) and isinstance(msg, str):
            raise ValueError('view warning input parameter')
        self.updateLabelWarning.emit(dirlabel,msg)

class plotDataContainer(object):
    '''
    This object contain two list need to plot,
    one is logged data list, the other is dynamic data list
    '''
    def __init__(self):
        super(plotDataContainer, self).__init__()
        self.dynamicAxis = ([],[],[])
        self.loggedAxis = ([],[],[])
        self.__tabState = False
        self.__startLog = False
        self.beginPlotTime = time.time()
        self.beginLogTime = False



    def get(self, x, y1, y2):
        if len(self.dynamicAxis[0]) < 1:
            self.beginPlotTime = x
        self.dynamicAxis[0].append(x-self.beginPlotTime)
        # print('begintime?', x, self.beginPlotTime)
        self.dynamicAxis[1].append(y1)
        self.dynamicAxis[2].append(y2)
        if self.__startLog == True:
            if not self.beginLogTime:
                self.beginLogTime = x
            self.loggedAxis[0].append(x - self.beginLogTime)
            self.loggedAxis[1].append(y1)
            self.loggedAxis[2].append(y2)

    def emit(self):
        def dynamicSlice(axis):
            lenaxis = len(axis[0])
            _slice = lenaxis/(100*(lenaxis**0.5))
            _slice = int(math.ceil(_slice))
            if _slice != 1:
                print('axis_slice',_slice)
            return _slice

        if self.__tabState == False:
            return [],[],[]
        elif self.__tabState == 'port':
            axis = self.dynamicAxis
            _slice = dynamicSlice(axis)
            return axis[0][::_slice], axis[1][::_slice], axis[2][::_slice]
        elif self.__tabState == 'log':
            if self.__startLog == True:
                axis = self.loggedAxis
                _slice = dynamicSlice(axis)
                return axis[0][::_slice], axis[1][::_slice], axis[2][::_slice]
            else:
                self._clearLoggedAxis()
                return [], [], []
        else:
            return [], [], []

    def clearDynamicAxis(self):
        if len(self.dynamicAxis[0]) > 0:
            self.dynamicAxis[0].clear()
            self.dynamicAxis[1].clear()
            self.dynamicAxis[2].clear()

    def _clearLoggedAxis(self):
        if len(self.loggedAxis[0]) > 0:
            self.loggedAxis[0].clear()
            self.loggedAxis[1].clear()
            self.loggedAxis[2].clear()
        self.beginLogTime = False
#
# state interface
#
    def setState(self, state):
        self.__tabState = state

    def setLogReStart(self, state):
        print ('__startlog', state)
        self.__startLog = state




class PowerDetector(object):
    '''
    :param detect is detect type
    :param serialNo is detect number or name, like vertical or inclined
    型号         |T0 【℃】| Z0 【mV/W】| Zc【（mV/W）/℃】
    B01-SMC| 20℃         | 50.3                | 0.088
    B05-SMC| 20℃         | 134.2              | 0.235
    C50-MC   | 20℃        | 0.59775          | 0.000747
    给出的temp实际上是电阻值单位kΩ，
    给出的功率power实际上是电压值单位为V'''

    def __init__(self, detect = 'C50-MC', serialNo = 'vertical'):
        object.__init__(self)
        para = {
        'B01-SMC': [20,50.3,0.088],
        'B05-SMC': [20,134.2,0.235],
        'C50-MC':   [20,0.59775,0.000747]}
        self.parameter = para[detect]

        self.slope, self.intercept = self._fitParaGet(serialNo)

    def _fitParaGet(self, serialNo):
        wrjson = WriteReadJson('data\\detector.json')
        jsonget = wrjson.load()
        if serialNo not in jsonget.keys():
            raise ValueError('detector json key error')
        paradict = jsonget.get(serialNo, {})
        if not paradict:
            raise ValueError('detector json parameter error')
        slope = paradict.get('slope', 0.0035)
        intercept = paradict.get('intercept', 0.0315)
        return slope, intercept

    def getPower(self, temp = 0, voltage = 0,):
        stand_temp, init_sen, correct_sen = self.parameter
        # temp = self.poly(temp)
        # Z = Z0 +（T-T0）*Zc
        sensitivity = init_sen +(temp-stand_temp)*correct_sen
        # voltage = (voltage*1000-8.977)/346.34
        voltage = voltage * 1000
        voltage = voltage * self.slope + self.intercept
        print('get slope', self.slope, self.intercept)
        # if voltage < 0.0001:
        #     print("voltage < 0")
        #     voltage = 0.0001
        #Φ = U/Z
        power = voltage/sensitivity
        #voltage 为探测器输出电压，单位是V，sensitivity 为探测器的灵敏度，单位是mV/W
        #power单位是mw?
        if power < 0.0001:
            power = 0.0001
        return power

    #1423
    def hex2power(self, heat, power):
        if not (isinstance(heat, bytes) or isinstance(power,bytes)):
            raise ValueError('para input error')
        heat = int().from_bytes(heat, 'little') / 100
        getPower = int().from_bytes(power, 'little')
        getPower = (getPower / 4096) * 3
        tmPower = self.getPower(heat, getPower)
        return tmPower


class DataSaveTick(threading.Thread,QObject):
    """docstring for DataSaveTick
    need a input dict which hold the data queue,
    pass the list to process and return a new list to get new data
    """
    resultEmite = pyqtSignal(object, object)

    def __init__(self,ticktime,dataGetDict):
        threading.Thread.__init__(self)
        QObject.__init__(self)
        super(DataSaveTick, self).__init__()
        self.daemon = True
        self.tick = ticktime
        self.dataGet = dataGetDict
        self.detector1 = PowerDetector(serialNo='inclined')
        self.detector2 = PowerDetector(serialNo='vertical')

    def run(self):
        '''rewrite this run() for a clock
        pass datalist to proccess per steptime
        '''
        while True:
            getlist = self.dataGet['dataGet']
            if len(getlist) > 2:
                self.factory(getlist)
                self.dataGet['dataGet'] = []
            time.sleep(self.tick)

    def factory(self,getlist):
        datalist1 = []
        datalist2 = []
        for x in getlist:
            # power: 14,23
            # print('len', len(x), x)
            if len(x[1]) < 9 :
                return
                # raise ValueError('x length error')
            power1 = self.detector1.hex2power(x[1][3:5],x[1][5:7])
            power2 = self.detector2.hex2power(x[1][1:3],x[1][7:9])

            # datalist.append([power,x[0],x[1]])
            datalist1.append(power1)
            datalist2.append(power2)
        datalist1.sort()
        datalist2.sort()
        end = int(len(datalist1) * 0.2)
        dataLen1 = len(datalist1[end:-end])
        powerresult1 = sum(datalist1)/(dataLen1)
        end = int(len(datalist2) * 0.1)
        dataLen2 = len(datalist2[end:-end])
        powerresult2 = sum(datalist2)/(dataLen2)
        getlist.clear()
        # print ('power result', powerresult)
        self.emitPower(powerresult1, powerresult2)


    def emitPower(self,powerresult1, powerresult2):
        # pass
        self.resultEmite.emit(powerresult1, powerresult2)