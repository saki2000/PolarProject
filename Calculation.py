from math import pi, sqrt
from tokenize import Double



class PositionCalculation():

    RADIUS = 40
    STEPS_PER_REVOLUTION = 96
    STEPPER_MOTOR_DISTANCE = 10000


    def __init__(self):

        self.circumference = 2*pi*float(self.RADIUS)
        self.stepDistance = self.circumference / int(self.STEPS_PER_REVOLUTION)
        self.currentPositionX = int(self.STEPPER_MOTOR_DISTANCE)
        self.currentPositionY = int(self.STEPPER_MOTOR_DISTANCE)
        self.currentCableLengthLeft = float(self.STEPPER_MOTOR_DISTANCE)
        self.currentCableLengthRight = float(self.STEPPER_MOTOR_DISTANCE)


    #function calculating left cable length using pythagoras therom

    def leftCableLength(self,positionX, positionY):

        cableLength = sqrt (positionX**2 + positionY**2)
        return cableLength


    #function calculating left cable length

    def rightCableLength(self, positionX, positionY):

        triangleBase = self.STEPPER_MOTOR_DISTANCE - positionX
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
            numberOfSteps = (newCableLength - self.currentCableLengthLeft) / self.stepDistance

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


        #prevents division by 0

        if numberOfStepsLeft == 0:
            numberOfStepsLeft =1

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

    def stepperMotorsData(self,positionX, positionY):
        
        numberOfStepsLeftMotor, directionLeft, newCableLengthLeft = self.leftMotorStepNumber(positionX, positionY)
        numberOfStepsRightMotor, directionRight, newCableLengthRight = self.rightMotorStepNumber(positionX, positionY)

        #obtaining ratio
        leftRatio, rightRatio = self.ratioCalculation(numberOfStepsLeftMotor, numberOfStepsRightMotor)

        # saving new cable lengths as current
        self.currentCableLengthLeft = newCableLengthLeft
        self.currentCableLengthRight = newCableLengthRight

        #Retrning data for both steppermotors
        #number of steps, direction, speed ratio
        return directionLeft, numberOfStepsLeftMotor, leftRatio, directionRight, numberOfStepsRightMotor, rightRatio



    #function resteing starting position

    def resetStartPosition(self):

        self.currentPositionX = 0
        self.currentPositionY = 0
        