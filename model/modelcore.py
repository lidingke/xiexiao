import  threading
import  queue
#from    time                import sleep
import time
import logging
# from    sys                 import exit
import pickle
# import sqlite3
import pdb
from    PyQt5.QtCore        import pyqtSignal, QObject
# from    PyQt5.QtCore        import QTime
# PySerial imports
import  serial

from  .lastlog import MsgSet

class ModelCore(threading.Thread, QObject):
    """docstring for ModelCore"""
    error = pyqtSignal(object)

    def __init__(self,port = 'com12'):
        threading.Thread.__init__(self)
        QObject.__init__(self)
        super(ModelCore, self).__init__()
        # print('is ModelCore __init__?')
        self.setDaemon(True)
        self.printText = queue.Queue()
        self.port = port
        self.br         = 9600
        self.timeout    = 0.001
        self.username = 'nobody'
        # PySerial object
        self.ser        = None
        # Flag for main cycle
        self.running    = True
        self.srcPortOpen = False
        self.pumpOpen = False
        self.isSerOpen = False
        # self.hexsplit = HexSplit.fun()

        # with open('data\\msg.pickle', 'rb') as f:
        #     entry = pickle.load(f)
        # self.msgDictHex = entry['msgDictHex']
        # print ('msg get ',self.msgDictHex)
        # self.msgDictStr = entry['msgDictStr']
        # self.sendmsgrec = entry['sendmsgrec']
        # self.entry = entry
        msgset = MsgSet()
        self.msgDictHex =msgset.getHexMsg()
        print('msg hex,', self.msgDictHex)

        self.__init__slaveStatus()


    def __init__slaveStatus(self):
        self.isSeedOpen = True
        self.seedcurrentre = False
        self.seedpulsere = False
        self.seedfrequecere = False
        self.seedcurrent = 0
        self.seedpulse = 0
        self.seedfrequece = 0
        self.firstcurrent = 0
        self.secondcurrent = 0
        self.isFirstPumpOpen = False
        self.isSecondPumpOpen = False
        self.isLEDOpen = False
        self.ti0 = 0

##########
#thread function
##########

    def run(self):
        '''
        Run thread.
            Method representing the thread's activity.
            You may override this method in a subclass. The standard run() method
            invokes the callable object passed to the object's constructor as the
            target argument, if any, with sequential and keyword arguments taken
            from the args and kwargs arguments, respectively.
        '''
        #
        while self.running:
            # print('started thread',self.ser)
            if self.ser:
                data = self.analysisbit()
                if data :
                    self.coreMsgProcess(data)
                    # print(HexSplit.fun(data.hex()))
            time.sleep(self.timeout)



    def stop(self):
        '''
        Stop thread.
        '''
        self.printShow('stop thread Model and close serial')

        if self.ser:
            self.ser.timeout = 0
            # change to non blocking mode and then close
            self.ser.close()

            self.ser = serial.Serial(baudrate=self.br, timeout=120)
        # self.ser = None
        self.running = False


    def begin(self):
        '''
        Initializate PySerial object
        '''
        self.ser = serial.Serial(baudrate=self.br, timeout=120)


##########
#global print
##########
    def printShow(self,*value,ifprint = True,text = True,nobyte = True):
        ''' print to CMD and text plain
        '''
        printlist = list()
        textlist = list()
        if value:
            for x in value:
                if type(x) == str:
                    printlist.append(x)
                    textlist.append(x)
                elif type(x) == int:
                    printlist.append(str(x))
                    textlist.append(str(x))
                elif type(x) == bytes:
                    # print(x)
                    # pdb.set_trace()
                    xhex = " ".join("{:02x}".format(c) for c in x)
                    textlist.append(xhex)
                    printlist.append(xhex)
                else:
                    printlist.append(str(x))
                    textlist.append(str(x))
            if ifprint:
                print(''.join(printlist))
            if text:
                printText = ''.join(textlist)
                if printText != ':bytes':
                    self.printText.put(printText)

#########
#port opration
#########

    def closePort(self):
        self.ser.close()

        # time.sleep(0.2)
        self.ser = serial.Serial(baudrate=self.br, timeout=120)
        # self.ser = None
        # print('iser open', self.ser.isOpen())
        self.printShow('ser=',self.ser)

    def reSetPort(self):
        try:
            print('reSetPort:',self.ser)
            self.ser = serial.Serial(self.port, self.br, timeout=120)
            # self.printShow(self.ser,text=False)
            self.printShow('port is open port name is ',self.port)
        except serial.serialutil.SerialException:
            self.printShow('=== can not open the port ===')
            self.ser = serial.Serial(baudrate=self.br, timeout=120)
            # self.printShow('ser=',self.ser)

            #self.stop()

    def isPortOpen(self):
        if self.ser:
            return self.ser.isOpen()
        else:
            return False



#############
#send message operation
############
    def write(self, data):
        '''
        data to send
        '''
        if type(data) is str:
            if data[:3] == 'msg':
                dataSend = b''.fromhex(data[4:])
            else:
                dataSend = self.msgcoup(data)
        else:
            dataSend =data
        if dataSend:
            self.printShow('上位机发送:',dataSend,text =False)
            try:
                if self.ser.isOpen():
                    self.ser.write(dataSend)
            except serial.serialutil.SerialException as e:
                # pdb.set_trace()
                print(e)
                    # if e == portNotOpenError:
                    #     raise e


        time.sleep(0.1)


    def readbit(self,ser):
        try:
            if self.ser and self.ser.isOpen():
                # print('ser, isopen',self.ser, self.ser.isOpen())
                data = self.ser.read(1)
            else:
                data = b'-1'
                time.sleep(0.1)
        except serial.serialutil.SerialException as e:
            # time.sleep(1)
            print(e)
            data = b'-1'
        except Exception as e:
            print(e)
            data = b'-1'
        return data

    def msgcoup(self,msg):
        '''package a message if msg length > 6
        '''
        msg = self.msgDictHex.get(msg, b'-1')
        if msg is b'-1':
            return msg
        else:
            if len(msg) > 6:
                return msg
            else:
                return b'\xEB\x90'+msg+b'\x90\xEB'

    def analysisbit(self):
        '''
                return without package
                input bit data analysis
        '''

        bitlist = list()
        while self.running:
            databit = self.readbit(self.ser)
            if databit == b'\xeb':
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
                    # print('tick ',tick)
                    if databit == b'\xA9':
                        if tick == 12:

                            data = b''.join(bitlist)
                            return b'\x9A' + data +b'\xA9'
                        else:
                            print('位数errror')
                            return b'0'
                    bitlist.append(databit)
        # return None


#interface
    def coreMsgProcess(self, *args, **kwargs):
        raise NotImplementedError

#==============================================================================
# Signals for view
#==============================================================================

    def emit_error(self, value):
        self.error.emit(value)

    def get_msgDict(self):
        return self.msgDictHex

    def get_port(self):
        return self.port

    def getEntry(self):
        return self.entry

    def get_br(self):
        return self.br

    def get_ser(self):
        return self.ser

    def get_queue(self):
        return self.printText

    def set_queue(self,queue_):
        # self.printText = qu()
        self.printText = queue_


    def setSer(self,ser):
        self.ser = ser

    def set_port(self,port):
        self.port = port

    def set_br(self, baudrate):
        self.br = baudrate

    def setUsername(self,name):
        self.username = name
        print('username is set: ',self.username)

# if __name__ == '__main__':
#     """is singleton"""
#     one = ModelCore()
#     two = ModelCore()
#     print('oneid',id(one))
#     print('twoid',id(two))
#     print(one == two)
