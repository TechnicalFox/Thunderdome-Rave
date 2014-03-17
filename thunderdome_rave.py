"""
Project Thunderdome: Sound & Lights

Objective: controll flashing/spinning lights and some speakers with
a raspberry pi

This implimentation by TechnicalFox.
"""

from pygame import mixer
import time
import sys
import RPi.GPIO as GPIO

"""
Class used to play audio and control lights on a raspberry pi.
"""
class thunderdome_rave(object):

    """
    Called when thunderdome_rave object is created.
    Sets variables, initialises the mixer, and
    loads in an audio file.
    """
    def __init__(self, pin):
        self.buisy = False
        self.fadeout = 5000
        mixer.init()
        mixer.music.load('/home/pi/Files/Thunderdome/siren.mp3')
    
        self.pin = pin
        self.commandDict = {                                         \
         'power': [9188,    4263,     784,     327,     804,     322,\
                    792,     340,     782,     318,     812,     321,\
                    783,     346,     787,     317,     814,     319,\
                    782,    1454,     812,    1459,     780,    1454,\
                    784,    1456,     807,    1455,     785,    1455,\
                    780,    1458,     809,    1452,     787,     319,\
                    812,     319,     784,    1456,     811,    1461,\
                    777,     325,     805,     323,     781,     350,\
                    782,     337,     793,    1458,     780,    1463,\
                    775,     351,     782,     337,     791,    1469,\
                    765,    1475,     771,    1471,     763,    1509,\
                    698],                                            \
     'rgbStrobe': [9208,    4300,     780,     350,     785,     322,\
                    813,     317,     792,     346,     790,     320,\
                    815,     324,     784,     353,     784,     321,\
                    813,    1462,     788,    1463,     784,    1460,\
                    821,    1459,     785,    1464,     784,    1465,\
                    810,    1464,     782,    1473,     776,     354,\
                    782,     328,     808,    1466,     783,     327,\
                    807,     328,     782,     353,     783,     336,\
                    804,     322,     783,    1530,     747,    1466,\
                    783,     338,     798,    1468,     776,    1486,\
                    770,    1474,     784,    1492,     719,    1534,\
                    714] }

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.OUT)
        self.microSecond = 0.000001
        self.gap = 96378.0 * self.microSecond

    """
    Pulses the GPIO pins of raspberry pi for specified
    amounts of time designated in above dict.
    """
    def pulse(self, command):
        commandList = self.commandDict[command]

        GPIO.output(self.pin, GPIO.HIGH)
        time.sleep(self.gap)

        count = 0
        for pulseTime in commandList:
            if count % 2 != 0:
                GPIO.output(self.pin, GPIO.HIGH)
            else:
                GPIO.output(self.pin, GPIO.LOW)

            time.sleep(pulseTime * self.microSecond)

            count += 1

            GPIO.output(self.pin, GPIO.HIGH)

    """
    Checks to see if it is ok to play audio due to
    time and if it is already playing something.
    """
    def can_play(self):
        answer = True
        hour = time.localtime().tm_hour
        if hour < 8 or hour > 22 or self.buisy: answer = False
        return answer
    
    """
    Plays the audio file specified in __init__.
    Checks with can_play first.
    """
    def play_siren(self, override=False):
        if self.can_play() or override:
            mixer.music.play()
            self.buisy = True

    """
    Stops audio being played. Does so by fading out
    for time period specified in __init__.
    """
    def stop_siren(self):
        if self.buisy:
            mixer.music.fadeout(self.fadeout)
            self.buisy = False

##################################
### END thunderdome_rave class ###
##################################

"""
Starts the thunderdome rave.
"""
def start_thunderdome_rave(sleepTime, debug=False):
    
    rgb = thunderdome_rave(12)
    if debug: print('\nrgbStrobe')
    for i in range(5):
        rgb.pulse('rgbStrobe')
    GPIO.cleanup()
    
    if debug: print('\nstart siren')
    rgb.play_siren(debug)
    
    if debug:
        print('\nsleeping for: ' + str(sleepTime))
        for i in range(sleepTime):
            if debug: print('sleep: ' + str(i+1))
            time.sleep(1)
    else: time.sleep(sleepTime)
    
    if debug: print('\nkill siren')
    rgb.stop_siren()
    
    power = thunderdome_rave(12)
    if debug: print('\npower')
    for i in range(5):
        power.pulse('power')
    GPIO.cleanup()
    
    sys.exit()

if __name__ == "__main__":
    try:
        if len(sys.argv) <= 2: start_thunderdome_rave(int(sys.argv[1]))
        else: start_thunderdome_rave(int(sys.argv[1]), bool(sys.argv[2]))
    except IndexError:
        print('You need to specify a sleep time in seconds.')
        sys.exit()
