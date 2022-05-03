import RPi.GPIO as GPIO
import time
from gpiozero import Servo 
from gpiozero.pins.pigpio import PiGPIOFactory



class Gondola:
    def __init__(self, pin,):

        factory = PiGPIOFactory()
        self.servo = Servo (pin, pin_factory=factory)
        #self.servo = Servo (pin, min_pulse_width = 0.5/1000, max_pulse_width = 2.5/1000, pin_factory=factory)


    def penDown(self):
        self.servo.max()


    def penUp(self):
        self.servo.min()






