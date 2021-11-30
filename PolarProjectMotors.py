import RPi.GPIO as GPIO
import time
import threading
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


class StepperMotor():               #Stepper Motor Class - Creating stepper motor object
    DELAY = 0.0025                  #Deley which pin is polarized bewteen steps
                                    #Halfstep sequnece
    HALFSTEP_SEQ = [[0,1,0,0], [0,1,0,1], [0,0,0,1], [1,0,0,1], [1,0,0,0], [0,0,1,1], [0,0,1,0], [0,1,1,0]]
    
    #Constructor taking pin numbers that stepper is connected to raspberry pi
    def __init__(self, pin_a, pin_b, pin_c, pin_d):     
        self.step_index = 1
        self.control_pins = [pin_a, pin_b, pin_c, pin_d]
        for pin in range(len(self.control_pins)):
            GPIO.setup(self.control_pins[pin], GPIO.OUT)
            GPIO.output(self.control_pins[pin], self.HALFSTEP_SEQ[self.step_index][pin])

    #half step sequence for stepper going left
    #stepping left is perforemd by following from last indext to first
    #when stepper reach first index in halfstep sequence, index changing to the very last
    def halfStepLeft(self, speed):
        self.step_index -= 1
        if self.step_index < 0:
            self.step_index = len(self.HALFSTEP_SEQ) - 1
        for pin in range(len(self.control_pins)):
            GPIO.output(self.control_pins[pin], self.HALFSTEP_SEQ[self.step_index][pin])
        time.sleep(self.DELAY + speed)

    #full step left
    def stepLeft(self,speed):
        self.halfStepLeft(speed)
        self.halfStepLeft(speed)

    #same as stepping left but going from first index to last - diffrent direction
    def halfStepRight(self, speed):
        self.step_index += 1                                  
        if self.step_index > len(self.HALFSTEP_SEQ) - 1:
            self.step_index = 0
        for pin in range(len(self.control_pins)):
            GPIO.output(self.control_pins[pin], self.HALFSTEP_SEQ[self.step_index][pin])
        time.sleep(self.DELAY + speed) 

    #full step right
    def stepRight(self,speed):
        self.halfStepRight(speed)
        self.halfStepRight(speed)

#function controling left stepper motor
#executes number of steps in given direction and speed
def leftStepperControl(direction, noOfSteps, speed):

    pointComplete = False

    if noOfSteps == 0:
        pointComplete = True

    while pointComplete == False:   #while loop to execute all steps passed 

        if(direction == "left"):    #if statment checking for direction
            leftStepper.stepLeft(speed)
            noOfSteps -= 1           
        else:
            leftStepper.stepRight(speed)
            noOfSteps -= 1   
        if noOfSteps == 0:
            pointComplete = True    #changing bool and ending while loop

#function controling right stepper motor
#executes number of steps in given direction and speed
def rightStepperControl(direction, noOfSteps, speed):

    pointComplete = False

    if noOfSteps == 0:
        pointComplete = True

    while pointComplete == False:

        if(direction == "left"):
            rightStepper.stepLeft(speed)
            noOfSteps -= 1
        else:
            rightStepper.stepRight(speed)
            noOfSteps -= 1   
        if noOfSteps == 0:
            pointComplete = True

#function calling in execution of stepper 
#motors in parralel
def stepperMotorsCall(lDirection,lNoofSteps,lSpeed,rdirection,rNoOfSteps,rSpeed):
    #creating threads for each stepper
    leftStepperThread = threading.Thread(target  = leftStepperControl, args=[lDirection,lNoofSteps,lSpeed] )
    rightStepperThread = threading.Thread(target = rightStepperControl, args=[rdirection,rNoOfSteps,rSpeed])

    leftStepperThread.start()
    rightStepperThread.start()

    #joining threads
    leftStepperThread.join()
    rightStepperThread.join()


def sample():
    stepperMotorsCall("left", 150,0.001, "left", 400,0)
    stepperMotorsCall("left", 50,0, "right", 200,0.0005)
    stepperMotorsCall("right", 500,0, "right", 500,0.005)
    stepperMotorsCall("left", 500,0.005, "left", 500,0)
    stepperMotorsCall("right", 500,0, "right", 100,0.0005)
    stepperMotorsCall("right", 400,0.0007, "right", 200,0)
    stepperMotorsCall("left", 500,0.0001, "left", 500,0)
    stepperMotorsCall("right", 400,0, "left", 200,0.0001)
    stepperMotorsCall("left", 200,0, "right", 600,0.0005)


#main menu
if __name__ == "__main__":

    leftStepper = StepperMotor(15, 18, 23, 24)
    rightStepper = StepperMotor(25, 8, 12, 16)

    


   

    