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
import led_controller as lights

"""
Class used to play audio and control lights on a raspberry pi.
"""
class thunderdome_rave(object):

    """
    Called when thunderdome_rave object is created.
    Sets variables, initialises the mixer, and
    loads in an audio file.
    """
    def __init__(self, override=False):
        self.buisy = False
        self.fadeout = 5000
        self.override = override
        mixer.init()
        mixer.music.load('/home/pi/Files/Thunderdome/siren.mp3')
    
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

    """
    Uses GPIO pins to power on an led strip to blink
    rgb colours.
    """
    def power_lights(self):
        print('on')
        x = lights.led_controller(12)
        for i in range(20):
            x.pulse('rgbStrobe')
        GPIO.cleanup()

    """
    Uses GPIO pins to power off an led strip.
    """
    def kill_lights(self):
        print('off')
        x = lights.led_controller(12)
        for i in range(20):
            x.pulse('power')
        GPIO.cleanup()
        

test = thunderdome_rave()
#test.power_lights()
#time.sleep(10)
test.kill_lights()
