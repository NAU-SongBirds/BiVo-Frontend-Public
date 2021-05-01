from io import UnsupportedOperation
import platform
import time
import serial
import serial.tools.list_ports
import sys
import serial
import glob


class newCom:
    def __init__(self):
        #Communication encoding for the Thunderboard
        self.COM_ENCODING = 'ISO-8859-1'
        #Amount of time until a serial operation times out
        self.SERIAL_TIMEOUT = .1
        #Baud rate for communication with Thunderboard
        self.BAUD_RATE = 115200
        #Serial Connection object to be initiated
        self.connection = None

#This does the handshake init for the available ports on a computer if it recieves an echo of the same message then it is successful and will connet to that port.
    def testInit(self):
        try:
            port = sys.argv[1]
            self.connection = serial.Serial( port=(port), baudrate=self.BAUD_RATE,
                                        timeout=self.SERIAL_TIMEOUT )
            # return true if connected
            sys.stdout.write(str(True))
        except serial.serialutil.SerialException:
            # return false if not connected
            sys.stdout.write(str(False))

connection = newCom()
connection.testInit()