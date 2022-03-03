from math import pi, sqrt
from tokenize import Double


RADIUS = 40
STEPS_PER_REVOLUTION = 96
STEPPER_MOTOR_DISTANCE = 30000



class PositionCalculation():


    def __init__(self):

        self.circumference = 2*pi*float(RADIUS)
        self.stepDistance = self.circumference / int(STEPS_PER_REVOLUTION)
        self.currentPositionX = int(STEPPER_MOTOR_DISTANCE)
        self.currentPositionY = int(STEPPER_MOTOR_DISTANCE)
        self.currentCableLengthLeft = float(STEPPER_MOTOR_DISTANCE)
        self.currentCableLengthRight = float(STEPPER_MOTOR_DISTANCE)


    #function calculating left cable length using pythagoras therom

    def leftCableLength(self,positionX, positionY):

        cableLength = sqrt (positionX**2 + positionY**2)
        return cableLength


    #function calculating left cable length

    def rightCableLength(self, positionX, positionY):
        
        triangleBase = STEPPER_MOTOR_DISTANCE - positionX
        cableLength = sqrt (triangleBase**2 + positionY**2)
        return cableLength


    #function calculate number of steps and direction for left stepper motor

    def leftMotorStepNumber(self, positionX, positionY):

        newCableLength = self.leftCableLength(positionX, positionY)

        if(newCableLength <= self.currentCableLengthLeft):
            direction = "left"
            numberOfSteps = (self.currentCableLengthLeft - newCableLength)  / self.stepDistance

        else:
            direction = "right"
            numberOfSteps = (newCableLength - self.currentCableLengthRight) / self.stepDistance

        return int(numberOfSteps), direction, newCableLength


    #function calculate number of steps and direction for left stepper motor\

    def rightMotorStepNumber(self, positionX, positionY):

        newCableLength = self.rightCableLength(positionX, positionY) #obtaining cable lenght

        if(newCableLength <= self.currentCableLengthRight):  #obtaining direction
            direction = "right"
            numberOfSteps =  (self.currentCableLengthRight - newCableLength) / self.stepDistance

        else:
            direction = "left"
            numberOfSteps = (newCableLength - self.currentCableLengthRight) / self.stepDistance

        return int(numberOfSteps), direction, newCableLength


    #function calculating ration - speed of stepper motor

    def ratioCalculation (self,numberOfStepsLeft, numberOfStepsRight):

        if(numberOfStepsLeft <= numberOfStepsRight):
            rightRatio = numberOfStepsRight
            leftRatio = numberOfStepsRight / numberOfStepsLeft

        else:
            leftRatio = numberOfStepsLeft
            rightRatio = numberOfStepsLeft / numberOfStepsRight

        return leftRatio, rightRatio


    #function resteing starting position

    def resetStartPosition(self):

        self.currentPositionX = 0
        self.currentPositionY = 0


    #function returning all the data for both stepper motors - speed, direction, ratio

    def stepperMotorsData(self,positionX, positionY):
        
        numberOfStepsLeftMotor, directionLeft, newCableLengthLeft = self.leftMotorStepNumber(positionX, positionY)
        numberOfStepsRightMotor, directionRight, newCableLengthRight = self.rightMotorStepNumber(positionX, positionY)
        
        #obtaining ratio
        leftRatio, rightRatio = self.ratioCalculation(numberOfStepsLeftMotor,numberOfStepsRightMotor)

        # saving new cable lengths as current
        self.leftCableLength = newCableLengthLeft
        self.rightCableLength = newCableLengthRight

        #Retrning data for both steppermotors
        #number of steps, direction, speed ratio
        return directionLeft, numberOfStepsLeftMotor, leftRatio, directionRight, numberOfStepsRightMotor, rightRatio
        
