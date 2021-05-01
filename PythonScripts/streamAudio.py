# removed imports that were used in the messy coded out area
from os import path
import os
import shutil
import wave
import struct
import platform

CHANNELS = 1 # 1 channel
RATE = 19900 # 19.9kHz sampling rate
wavFileGenerated = ""

def createOutputFolder():
    try:
        # make a folder named "Audio" in the current directory
        os.mkdir('Audio')

    except FileExistsError:
        # handle FileExistsError exception
        # do nothing if folder named 'Audio' exists already
        pass

def getWavFileName():
    # number to append to end of existing file names
    counter = 0
    # default base name o the wav files
    filename = "audio_segment{}.wav"
    # Checks to see if specified path is an existing file
    # specifically look in the Audio directory
    audioStr = ""

    if(platform.system() == 'Windows'):
        audioStr = "Audio\\"

    else:
        audioStr = "Audio/"

    while os.path.isfile(audioStr + filename.format(counter)):
        # if specified path holds an existing file
        # increment number to be appended at end of file name
        counter += 1
    # insert counter value to placeholder in file name string
    filename = filename.format(counter)
    return filename

def moveFileToAudioDir(fileName):
    slashStr = ""
    if(platform.system() == 'Windows'):
        slashStr = "\\"
    else:
        slashStr = "/"
    # get current path to file
    # append file name to current working directory path
    src = os.getcwd() + slashStr + fileName
    # set up destination (to the Audio directory)
    # append together the current working directory, audio directory, and file name 
    dst = os.getcwd() + slashStr + "Audio" + slashStr + fileName
    # perform the move from source path to destination path
    shutil.move(src, dst)

def createWavFile(audioArr):
    wavFileName = getWavFileName()
    # save the audio data as .wav file
    wavefile = wave.open(wavFileName,'wb')
    wavefile.setnchannels(CHANNELS)
    wavefile.setsampwidth(2)
    wavefile.setframerate(RATE)
    wavefile.writeframes(audioArr)
    wavefile.close()
    # move the created wav file to the Audio directory
    moveFileToAudioDir(wavFileName)
    return wavFileName

# not in use
# def generateAudioSegment(receivedByteArr):
#     # Create Audio Output folder to store the audio segment in
#     createOutputFolder()
#     # Create the wav file based on the received array and save in Audio folder
#     createWavFile(receivedByteArr)

#                                                                                             #
#               SUPER DUPER MESSY CODE I DON'T USE OR HAVE TRIED TO MESS WITH                 # 
#                                                                                             #




# def addMetaData(fileName):
#     audio = mutagen.File(fileName, easy=True)

#     # only if audio file does not have tags already (blank slate)
#     # audio.add_tags()

#     # My custome ID3 tags that are not considered valid keys for mutagen
#     EasyID3.RegisterTXXXKey('sensorid', 'SENSORID')
#     EasyID3.RegisterTXXXKey('time', 'TIME')

#     # Assign tags
#     audio['sensorid'] = "1"
#     audio['time'] = "now"

#     # Save changes
#     audio.save(fileName, v1=2)

#     print(audio['date'])
#     print(audio['sensorid'])
#     print(audio['time'])

# addMetaData("nature.mp3")

# convert wav to mp3                                                            
# sound = AudioSegment.from_mp3("nature.mp3")
# sound.export("naturetest.wav", format="wav")


# f = music_tag.load_file("naturetest.wav")
# print(f['sensorid'])
# print(f['time'])

# used for pyaudio testing
#find index of thunderboard
# p = pyaudio.PyAudio()
# for ii in range(p.get_device_count()):
#     print(p.get_device_info_by_index(ii))