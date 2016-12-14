from unittest import TestCase
from model.modelcore import ModelCore
from PyQt5.QtCore import QObject
import  serial

class TestModelCore(TestCase):

    def setUp(self):
        self.model = ModelCore()
        assert hasattr(self.model,'running')
        self.assertIsInstance(self.model,QObject)

    # def test_stop(self):
    #     self.fail()
    #
    def test_begin(self):
        self.assertIsInstance(self.model.ser,serial.Serial)
    #
    def test_closePort(self):
        self.model.reSetPort('com15')
    #
    # def test_write(self):
    #     self.fail()
    #
    # def test_readbit(self):
    #     self.fail()
