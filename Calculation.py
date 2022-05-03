from math import pi, sqrt
from tkinter import Scale
from tokenize import Double



class PositionCalculation():

    RADIUS = 5
    STEPS_PER_REVOLUTION = 192
    STEPPER_MOTOR_DISTANCE = 795
<<<<<<< HEAD
    
=======

>>>>>>> 1964b3f89373cf46e186238596f60d0bc5a3f014

    def __init__(self):

        self.scale = 0.06
        self.circumference = 2*pi*float(self.RADIUS)
        self.stepDistance = self.circumference / self.STEPS_PER_REVOLUTION
<<<<<<< HEAD
        self.currentPositionX = 20 #int(self.STEPPER_MOTOR_DISTANCE)
        self.currentPositionY =  20 #int(self.STEPPER_MOTOR_DISTANCE)
=======
        self.currentPositionX = int(self.STEPPER_MOTOR_DISTANCE)
        self.currentPositionY = int(self.STEPPER_MOTOR_DISTANCE)
>>>>>>> 1964b3f89373cf46e186238596f60d0bc5a3f014
        self.currentCableLengthLeft = self.getLeftCableLength(self.currentPositionX, self.currentPositionY)
        self.currentCableLengthRight = self.getRightCableLength(self.currentPositionX, self.currentPositionY)


    #function calculating left cable length using pythagoras therom

    def getLeftCableLength(self,positionX, positionY):

        cableLength = sqrt (positionX**2 + positionY**2)
        return cableLength


    #function calculating left cable length

    def getRightCableLength(self, positionX, positionY):

        triangleBase = self.STEPPER_MOTOR_DISTANCE - positionX
        cableLength = sqrt (triangleBase**2 + positionY**2)
        return cableLength


    #function calculate number of steps and direction for left stepper motor

    def getLeftMotorData(self, positionX, positionY):

        newCableLength = self.getLeftCableLength(positionX, positionY)

        if(newCableLength <= self.currentCableLengthLeft):
            direction = "left"
            numberOfSteps = (self.currentCableLengthLeft - newCableLength)  / self.stepDistance

        else:
            direction = "right"
            numberOfSteps = (newCableLength - self.currentCableLengthLeft) / self.stepDistance

        return int(numberOfSteps), direction, newCableLength


    #function calculate number of steps and direction for left stepper motor\

    def getRightMotorData(self, positionX, positionY):

        newCableLength = self.getRightCableLength(positionX, positionY) #obtaining cable lenght

        if(newCableLength <= self.currentCableLengthRight):  #obtaining direction
            direction = "right"
            numberOfSteps =  (self.currentCableLengthRight - newCableLength) / self.stepDistance

        else:
            direction = "left"
            numberOfSteps = (newCableLength - self.currentCableLengthRight) / self.stepDistance

        return int(numberOfSteps), direction, newCableLength


    #function calculating ration - speed of stepper motor

    def getSpeedRatio (self,numberOfStepsLeft, numberOfStepsRight):

        #prevents division by 0

        if numberOfStepsLeft == 0:
            numberOfStepsLeft = 1

        if numberOfStepsRight == 0:
            numberOfStepsRight = 1

        if(numberOfStepsLeft <= numberOfStepsRight):
            rightRatio = 1
            leftRatio = numberOfStepsRight / numberOfStepsLeft

        else:
            leftRatio = 1
            rightRatio = numberOfStepsLeft / numberOfStepsRight

        return leftRatio, rightRatio


    #function returning all the data for both stepper motors - speed, direction, ratio
    def getMotorsData(self,positionX, positionY):

        #immplementing pictre scale
        positionX = int(positionX * self.scale)
        positionY = int(positionY * self.scale)
        
        numberOfStepsLeftMotor, directionLeft, newCableLengthLeft = self.getLeftMotorData(positionX, positionY)
        numberOfStepsRightMotor, directionRight, newCableLengthRight = self.getRightMotorData(positionX, positionY)

        #obtaining ratio
        leftRatio, rightRatio = self.getSpeedRatio(numberOfStepsLeftMotor, numberOfStepsRightMotor)

        # saving new cable lengths as current and updating new position
        self.currentCableLengthLeft = newCableLengthLeft
        self.currentCableLengthRight = newCableLengthRight
        self.currentPositionX = positionX
        self.currentPositionY = positionY

        #Retrning data for both steppermotors
        #number of steps, direction, speed ratio
        return directionLeft, numberOfStepsLeftMotor, leftRatio, directionRight, numberOfStepsRightMotor, rightRatio


    #function resteing starting position

    def resetStartPosition(self):

        self.currentPositionX = 0
        self.currentPositionY = 0
        self.currentCableLengthLeft = self.getLeftCableLength(self.currentPositionX, self.currentPositionY)
        self.currentCableLengthRight = self.getRightCableLength(self.currentPositionX, self.currentPositionY)
        
