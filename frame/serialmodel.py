import serial
import threading

class SerialModel(threading.Thread):
    """abstract basic serial model"""
    def __init__(self, ):
        super(SerialModel, self).__init__()
        # self.daemon = True
        self.port = False
        self.baundrate = 9600
        self.ser = False
        self._initPort()
        self.running = True
        self.data = b'-1'

    def _initPort(self):
        """set default baundrate 9600, default port None"""
        if self.port:
            self._setPort(self.port, self.baundrate)

    def _setPort(self, port, baundrate):

        if port:
            self.ser = serial.Serial(port = port, baudrate=baundrate, timeout=120)
            print('get ser', self.ser)
        else:
            self.ser = serial.Serial(baudrate=baundrate, timeout=120)

    def setPort(self, port, baundrate):
        try:
            self._setPort(port, baundrate)
        except serial.serialutil.SerialException:
            print("can't set port correct")


    def _write(self, bitDatas):
        if self.ser and self.ser.isOpen() and bitDatas:
            self.ser.write(bitDatas)


    def _readBit(self):
        if self.ser and self.ser.isOpen():
            return self.ser.read(1)
        else:
            return b'-1'

    def run(self):
        raise NotImplementedError

    def close(self):
        self.running = False
        if isinstance(self.ser, serial.Serial):
            self.ser.close()
            self.ser = serial.Serial(baudrate=self.baundrate, timeout=120)


