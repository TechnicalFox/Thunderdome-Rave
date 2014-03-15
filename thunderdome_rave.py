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
    def __init__(self, pin, override=False):
        self.buisy = False
        self.fadeout = 5000
        self.override = override
        mixer.init()
        mixer.music.load('/home/pi/Files/Thunderdome/siren.mp3')
    
        self.pin = pin
        self.commandDict = {                                         \
         'power': [9043,    4518,     531,     518,     577,     557,\
                    568,     541,     587,     538,     572,     556,\
                    569,     548,     583,     531,     599,     532,\
                    579,    1664,     594,    1658,     576,    1672,\
                    569,    1667,     571,    1706,     563,    1664,\
                    573,    1666,     574,    1680,     577,     534,\
                    573,     557,     570,    1698,     546,    1675,\
                    590,     524,     572,     558,     574,     547,\
                    584,     532,     580,    1708,     549,    1670,\
                    564,     582,     550,     536,     591,    1666,\
                    582,    1666,     569,    1664,     575,    1673,\
                    583],                                            \
           'red': [9034,    4443,     598,     528,     575,     554,\
                    567,     547,     587,     532,     560,     566,\
                    565,     552,     586,     529,     563,     568,\
                    562,    1675,     564,    1702,     567,    1662,\
                    569,    1661,     581,    1667,     581,    1665,\
                    574,    1661,     574,    1678,     574,     539,\
                    572,     556,     573,     538,     593,    1666,\
                    582,    1653,     565,     556,     581,    1654,\
                    582,     547,     570,    1662,     580,    1673,\
                    581,    1672,     570,     548,     582,     526,\
                    581,    1669,     586,     525,     570,    1677,\
                    596],                                            \
          'blue': [9047,    4445,     604,     519,     596,     535,\
                    571,     536,     593,     533,     574,     555,\
                    574,     545,     618,     497,     573,     559,\
                    587,    1650,     578,    1676,     576,    1670,\
                    574,    1669,     570,    1685,     576,    1667,\
                    569,    1667,     574,    1672,     589,    1668,\
                    571,     582,     554,    1661,     575,     541,\
                    588,     531,     573,     557,     574,    1677,\
                    562,     561,     574,     537,     590,    1661,\
                    578,     538,     594,    1659,     574,    1663,\
                    582,    1671,     587,     532,     569,    1680,\
                    581],                                            \
     'rgbStrobe': [9029,    4448,     616,     505,     584,     545,\
                    593,     513,     595,     530,     581,     548,\
                    576,     537,     581,     540,     575,     553,\
                    571,    1672,     571,    1668,     590,    1668,\
                    571,    1664,     584,    1658,     587,    1663,\
                    576,    1658,     576,    1675,     587,     531,\
                    584,     545,     571,    1667,     583,     544,\
                    572,     533,     599,     525,     576,     554,\
                    578,     535,     594,    1658,     573,    1662,\
                    584,     546,     593,    1641,     582,    1660,\
                    592,    1670,     569,    1662,     585,    1656,\
                    604] }

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
        if hour < 8 or hour > 22: answer = False
        if self.buisy == True: answer = False
        return answer
    
    """
    Plays the audio file specified in __init__.
    Checks with can_play first.
    """
    def play_siren(self):
        if self.can_play() or self.override:
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


test = thunderdome_rave(12)
for i in range(10):
    test.pulse('red')
GPIO.cleanup()

sys.exit()
