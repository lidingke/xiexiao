from unittest import TestCase
from model.modelpump import ModelPump

class TestModelPump(TestCase):

    def setUp(self):
        self.model = ModelPump()

    def test_open_port(self):
        pass


    def tearDown(self):
        self.model.close()
