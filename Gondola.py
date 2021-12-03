import RPi.GPIO as GPIO
import time




class Gondola:
    def __init__(self, pin):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)  
        GPIO.setup(pin, GPIO.OUT)

        #setting up  GPIO output with 50hz  pulse
        self.servo = GPIO.PWM(pin,50)
        self.servo.start(0)


    def penDown(self):
        self.servo.ChangeDutyCycle(1)

    def penUp(self):
        self.servo.ChangeDutyCycle(6)


gondola = Gondola(21)
#gondola.penDown()
time.sleep(10)
#gondola.penUp()





