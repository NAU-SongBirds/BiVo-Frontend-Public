from NewCom import newCom
import sys
from streamAudio import createOutputFolder, createWavFile

#This file is run by the MatLab GUI to collect an audio segment form the board and save the Wav file

#Create a new connection object to handle the serial input
connection = newCom()
#Initalize the connection object within the connection class
connection.testInit()
#Recieve an audio segment
connection.getAudio()
#Return the audio array from the board
audioArr = connection.returnAudio()
#Create an output Audio folder
createOutputFolder()
# Create the wav file based on the received array and save in Audio folder
# Let GUI know what audio segment generated
sys.stdout.write(str(createWavFile(audioArr)))