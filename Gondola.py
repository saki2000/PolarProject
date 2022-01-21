import RPi.GPIO as GPIO
import time
from gpiozero import Servo 
from gpiozero.pins.pigpio import PiGPIOFactory



class Gondola:
    def __init__(self, pin,):

        factory = PiGPIOFactory()
        self.servo = Servo (pin, pin_factory=factory)


    def penDown(self):
        self.servo.max()


    def penUp(self):
        self.servo.min()
        

    def test (self):
        time.sleep(1)
        self.penDown()
        time.sleep(1)
        self.penUp()
        time.sleep(1)
        self.penDown()
        time.sleep(1)
        self.penUp()
        time.sleep(1)
        self.penDown()
        time.sleep(1)
        self.penUp()
        time.sleep(1)
        self.penDown()
        time.sleep(1)
        self.penUp()






