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



gondola = Gondola(12)
time.sleep(1)
gondola.penDown()
time.sleep(1)
gondola.penUp()
time.sleep(1)
gondola.penDown()
time.sleep(1)
gondola.penUp()
time.sleep(1)
gondola.penDown()
time.sleep(1)
gondola.penUp()
time.sleep(1)
gondola.penDown()
time.sleep(1)
gondola.penUp()

