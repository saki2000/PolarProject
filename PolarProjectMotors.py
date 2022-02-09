import RPi.GPIO as GPIO
import time



class StepperMotor():               #Stepper Motor Class - Creating stepper motor object
    DELAY = 0.0025                  #Deley which pin is polarized bewteen steps
                                    #Halfstep sequnece
    HALFSTEP_SEQ = [[0,1,0,0], [0,1,0,1], [0,0,0,1], [1,0,0,1], [1,0,0,0], [0,0,1,1], [0,0,1,0], [0,1,1,0]]
    stopMotor = False
    

    #Constructor taking pin numbers that stepper is connected to raspberry pi
    def __init__(self, pin_a, pin_b, pin_c, pin_d):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)   
        self.step_index = 1
        self.control_pins = [pin_a, pin_b, pin_c, pin_d]
        for pin in range(len(self.control_pins)):
            GPIO.setup(self.control_pins[pin], GPIO.OUT)
            GPIO.output(self.control_pins[pin], self.HALFSTEP_SEQ[self.step_index][pin])


    #half step sequence for stepper going left
    #stepping left is perforemd by following from last indext to first
    #when stepper reach first index in halfstep sequence, index changing to the very last
    def halfStepLeft(self, speedRatio):
        self.step_index -= 1
        if self.step_index < 0:
            self.step_index = len(self.HALFSTEP_SEQ) - 1
        for pin in range(len(self.control_pins)):
            GPIO.output(self.control_pins[pin], self.HALFSTEP_SEQ[self.step_index][pin])
        time.sleep(self.DELAY / speedRatio)


    #full step left
    def stepLeft(self,speedRatio):
        self.halfStepLeft(speedRatio)
        self.halfStepLeft(speedRatio)


    #same as stepping left but going from first index to last - diffrent direction
    def halfStepRight(self, speedRatio):
        self.step_index += 1                                  
        if self.step_index > len(self.HALFSTEP_SEQ) - 1:
            self.step_index = 0
        for pin in range(len(self.control_pins)):
            GPIO.output(self.control_pins[pin], self.HALFSTEP_SEQ[self.step_index][pin])
        time.sleep(self.DELAY / speedRatio) 


    #full step right
    def stepRight(self,speedRatio):
        self.halfStepRight(speedRatio)
        self.halfStepRight(speedRatio)


    #function controling left stepper motor
    #executes number of steps in given direction and speed
    def stepperControl(self,direction, noOfSteps, speedRatio):

        pointComplete = False

        if noOfSteps == 0:
            pointComplete = True

        while pointComplete == False:   #while loop to execute all steps passed 

            if(direction == "left"):    #if statment checking for direction
                self.stepLeft(speedRatio)
                noOfSteps -= 1           
            else:
                self.stepRight(speedRatio)
                noOfSteps -= 1   
            if noOfSteps == 0:
                pointComplete = True    #changing bool and ending while loop

    
    def stopMotors(self):
        self.stopMotor = True

    def startMotors(self):
        self.stopMotor = False

   

    