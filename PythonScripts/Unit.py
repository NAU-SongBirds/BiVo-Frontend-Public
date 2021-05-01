import unittest
from NewCom import newCom
from unittest.mock import patch

class TestCom(unittest.TestCase):

    @patch('platform.platform')
    @patch('serial.Serial')
    def testWindowsInit(self,serialMock,platformMock):
        com = newCom()
        serialMock.return_value = "connected"
        platformMock.return_value = "Windows"
        com.initConnection()
        assert com.connection == "connected"
    
    @patch('platform.platform')
    @patch('serial.Serial')
    def testMacInit(self,serialMock,platformMock):
        com = newCom()
        serialMock.return_value = "connected"
        platformMock.return_value = "mac"
        com.initConnection()
        assert com.connection == "connected"
    
    @patch('platform.platform')
    @patch('serial.Serial')
    def testUnsupportedInit(self,serialMock,platformMock):
        com = newCom()
        serialMock.return_value = "connected"
        platformMock.return_value = "unsupported"
        with self.assertRaises(Exception):
            com.initConnection()

if __name__ == "__main__":
    unittest.main()