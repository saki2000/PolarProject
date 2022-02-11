from tkinter import filedialog
from math import pi, sqrt
from tokenize import Double

RADIUS = 40
STEPS_PER_REVOLUTION = 96
STEPPER_MOTOR_DISTANCE = 30000

class DataProccessing():

    splitData = []

    #function loading data from the hpgl file
    #using tkinter opendialog to open window to load a file

    def loadData(self):
        self.dataFile = filedialog.askopenfilename(filetypes=(("HPGL Files", "*.hpgl"),))
        self.dataFile = open(self.dataFile, 'r')
        dataPoints = self.dataFile.read()           #reading from the file
        self.dataFile.close()                       #closing file
        splitData = dataPoints.split(";")           #spliting data on each occurance of ;

        print (splitData)


   # def switchOptions(command):
   #     match command:
            

class PositionCalculation():

    currentPositionX = 0
    currentPositionY = 0
    currentCableLengthLeft = 0.0
    currentCableLengthRight = 0.0
    circumference = 0.0
    stepDistance = 0.0


    def __init__(self):

        circumference = 2*pi*RADIUS
        stepDistnace = circumference / STEPS_PER_REVOLUTION
        currentPositionX = STEPPER_MOTOR_DISTANCE
        currentPositionY = STEPPER_MOTOR_DISTANCE
        currentCableLengthLeft = self.leftCableLength(currentPositionX, currentPositionY)
        currentCableLengthRight = self.rightCableLength(currentPositionX, currentPositionY)


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

        return numberOfSteps, direction, newCableLength


    #function calculate number of steps and direction for left stepper motor\

    def rightMotorStepNumber(self, positionX, positionY):

        newCableLength = self.rightCableLength(positionX, positionY)

        if(newCableLength <= self.currentCableLengthRight):
            direction = "right"
            numberOfSteps =  (self.currentCableLengthRight - newCableLength) / self.stepDistance

        else:
            direction = "left"
            numberOfSteps = (newCableLength - self.currentCableLengthRight) / self.stepDistance

        return numberOfSteps, direction, newCableLength


    #function calculating ration - speed of stepper motor

    def ratioCalculation (numberOfStepsLeft, numberOfStepsRight):

        if(numberOfStepsLeft <= numberOfStepsRight):
            rightRatio = numberOfStepsRight
            leftRatio = numberOfStepsRight / numberOfStepsLeft

        else:
            leftRatio = numberOfStepsLeft
            rightRatio = numberOfStepsLeft / numberOfStepsRight

        return leftRatio, rightRatio


    #function resteing starting position

    def resetStartPosition(self):

        currentPositionX = 0
        currentPositionY = 0
        