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
        #Holds the byte data that will be recieved from the board
        self.dataBuffer = bytearray()
        #Message to send to board to handshake with it
        self.handShakeMessage = "hands"
        #Message to recieve from board to continue handshake
        self.handShakeConfirm = "cnfrm"
        #Message to send to board to ackowledge handshake
        self.handShakeAck = "ackng"
        #Command to record audio on the board
        self.audioMessage = "recrd"
        #Message recieved from board to indicate an end of audio segments
        self.endMessage = "-end-"


#Credit to https://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python which shows how to list coms for different operating systems
#Lists the comports on an operating system and returns a list of all the ones that currently have a connection.
    def listPorts(self):
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')
        result = []
        for port in ports:
            try:
                #Check if we can make a serial port object
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

#This does the handshake init for the available ports on a computer if it recieves an echo of the same message then it is successful and will connet to that port.
    def testInit(self):
        availablePorts = self.listPorts()
        for port in availablePorts:
            try:
                #Create a serial port object with one port from the list of available
                self.connection = serial.Serial(port = port, baudrate = self.BAUD_RATE,
                                            timeout = self.SERIAL_TIMEOUT)
                #Write the handshake to the boards serial
                self.connection.write(self.handShakeMessage.encode(self.COM_ENCODING))
                #Read the hanshake confirm from the serial
                board_input = self.connection.read(len(self.handShakeConfirm))
                #Check if that input is the expected input, if so write back the ackowledge
                if board_input.decode(self.COM_ENCODING) == self.handShakeConfirm:                    
                    self.connection.write(self.handShakeAck.encode(self.COM_ENCODING))
                    break
            except serial.serialutil.SerialException:
                pass

#Sends a get audio message to the board and accepts audio data immediately after and stops if endMessage is found at the end of the data buffer
    def getAudio(self):
        incomingData = bytearray()
        try:
            self.connection.write(self.audioMessage.encode(self.COM_ENCODING))
            while True:
                #add data from serial port as long as theres something there
                incomingData = self.connection.read(self.connection.inWaiting())
                #Append the serial data onto the data buffer
                self.dataBuffer+=(incomingData)
                #Check if thre is enough data to check the end of the data buffer
                if(len(self.dataBuffer) > len(self.endMessage)):
                    #Check the last bytes of the databuffer if it is the end message string
                    if self.dataBuffer[-len(self.endMessage):].decode(self.COM_ENCODING) == self.endMessage:
                        #Stop the buffer collection, Only gather the audio, no end message in data buffer.
                        self.dataBuffer = self.dataBuffer[0:-len(self.endMessage)]
                        break
                
        except serial.serialutil.SerialException as e:
            print( "\n\nSomething went wrong! :-(  ",
                "You may have unplugged the board.\n\n" )
            exit(1)

#returns the audio so that the GUI can recieve the audio segment.
    def returnAudio(self):
        return self.dataBuffer
