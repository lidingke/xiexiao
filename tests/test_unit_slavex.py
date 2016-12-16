import time
import threading
import serial
from slave.slavex import SlaveX

from frame.serialmodel import SerialModel
import unittest
import pytest

class SlaveXTest(unittest.TestCase):

    def setUp(self):
        self.testthread = TThread()
        self.testthread.start()
        self.testthread.setPort('com15',9600)
        self.source = SlaveX()
        self.source.start()
        self.source.setPort('com16',9600)

    def test_slave_port_open(self):
        assert hasattr(self.testthread,'ser')
        assert hasattr(self.testthread.ser,'port')
        assert isinstance(self.testthread.ser, serial.Serial)
        assert self.testthread.ser.port == self.testthread.port
        assert self.source.ser.port == self.source.port



    def test_serial_source_write(self):
        print(self.source.ser,self.testthread.ser, self.testthread.port)
        self.testthread._write(b"\xEB\x90\x01\x00\x00\x01\x90\xEB")
        time.sleep(0.2)
        assert self.source.data == b'\x01\x00\x00\x01'

    def tearDown(self):
        self.testthread.close()
        self.source.close()


class TThread(SerialModel):
    """docstring for Source"""
    def __init__(self, ):
        super(TThread, self).__init__()
        self.running = True
        # self.setPort('com15', 9600)
        self.port = 'com15'
        self.baundrate = 9600
        self.setDaemon(True)
        print('tthread', self.port)

    def run(self):
        while self.running:
            time.sleep(0.1)

if __name__ == '__main__':
    unittest.main()



