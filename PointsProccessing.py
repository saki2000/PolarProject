import time
from tkinter import filedialog
import threading
from types import LambdaType

from PolarProjectMotors import StepperMotor
from Calculation import PositionCalculation
from Gondola import Gondola




class DataProccessing:

    def __init__(self):

        self.leftStepper = StepperMotor(15, 18, 23, 24)
        self.rightStepper = StepperMotor(25, 8, 12, 16)
        self.splitData = []
        self.positionCalculation = PositionCalculation()
        self.gondola = Gondola(7)

    #function loading data from the hpgl file
    #using tkinter opendialog to open window to load a file

    def loadData(self):
        self.dataFile = filedialog.askopenfilename(filetypes=(("HPGL Files", "*.hpgl"),))
        self.dataFile = open(self.dataFile, 'r')
        dataPoints = self.dataFile.read()           #reading from the file
        self.dataFile.close()                       #closing file
        self.splitData = dataPoints.split(";")           #spliting data on each occurance of ;

    #function calling in execution of stepper 
    #motors in parralel
    def stepperMotorsCall(self,lDirection,lNoOfSteps,lSpeed,rDirection,rNoOfSteps,rSpeed):

        if (self.rightStepper.stopMotor == False):

            #creating threads for each stepper and passing data for each step
            leftStepperThread = threading.Thread(target  = self.leftStepper.stepperControl, args=[lDirection,lNoOfSteps,lSpeed], daemon = True )
            rightStepperThread = threading.Thread(target = self.rightStepper.stepperControl, args=[rDirection,rNoOfSteps,rSpeed], daemon = True)

            leftStepperThread.start()
            rightStepperThread.start()

            #joining threads
            leftStepperThread.join()
            rightStepperThread.join()
        
    

    #interpreting all commands for loaded list - splitData

    def executeFile(self):

        for num in range(len(self.splitData)):   #for loop going through all the commands(elements) in the list

            command = self.splitData[num][0:2]

            #initialise start and zero satarting position to current gondola position (0,0)

            if command == "IN":
                self.positionCalculation.resetStartPosition()
                print("command IN")
                continue

            #printing pen number information

            elif command == "SP":
                print('Pen number: %s  selected' %self.splitData[num][2:])
                continue
            
            #Pen up
            #go to positions in the list

            elif command == "PU":
                self.gondola.penUp()
                time.sleep(1)
                positions  = self.splitData[num][2:]    #Spliting data to get only x,y values
                positionsList = positions.split(',')
                
                #prevents crash when command has no parameters
                if (len(positionsList) == 0 or len(positionsList) == 1):
                    continue

                for n in range (0,len(positionsList),2):

                    #prevents division by zero
                    if(positionsList[n] == "0" and positionsList[n+1] == "0"):
                        continue
                    
                    #geting data from the calcualtion object and calling motors to execute step
                    else:
                        
                        #getting data for stepper motors
                        directionLeft, numberOfStepsLeftMotor, leftRatio, directionRight, numberOfStepsRightMotor, rightRatio = self.positionCalculation.getMotorsData(int(positionsList[n]), int(positionsList[n+1]))

                        #caling motors to execute step with calculated data
                        self.stepperMotorsCall(directionLeft, numberOfStepsLeftMotor, leftRatio, directionRight, numberOfStepsRightMotor, rightRatio)
                        
                continue

            #Pen down
            #Draw following position in command list

            elif command == "PD":
                self.gondola.penDown()
                time.sleep(1)
                positions  = self.splitData[num][2:]
                positionsList = positions.split(',')
                
                #prevents crash when command has no parameters
                if (len(positionsList) == 0 or len(positionsList) == 1):
                    continue
                
                for n in range (0,len(positionsList),2):

                    #prevents division by zero
                    if(positionsList[n] == "0" and positionsList[n+1] == "0"):
                        continue

                    print("Current position:  x= ",self.positionCalculation.currentPositionX,"y= ", self.positionCalculation.currentPositionY )
                    print("Moving to position: x=",positionsList[n], "y=",positionsList[n+1])
                    print("Current cable lengths: Left motor: ",self.positionCalculation.currentCableLengthLeft, "Right: ", self.positionCalculation.currentCableLengthRight)

                    #getting data from calculation to control stepper motor.
                    directionLeft, numberOfStepsLeftMotor, leftRatio, directionRight, numberOfStepsRightMotor, rightRatio = self.positionCalculation.getMotorsData(int(positionsList[n]), int(positionsList[n+1]))
                    
                    print("LEFT: ","dir: ", directionLeft,"steps: ", numberOfStepsLeftMotor,"ratio: ", leftRatio)
                    print("RIGHT: ","dir: ", directionRight,"steps:", numberOfStepsRightMotor,"ratio: ", rightRatio)
                    
                    #calling to execute calculated step
                    self.stepperMotorsCall(directionLeft, numberOfStepsLeftMotor, leftRatio, directionRight, numberOfStepsRightMotor, rightRatio)

                    print("New cable lengths: Left: ",self.positionCalculation.currentCableLengthLeft, "Right: ", self.positionCalculation.currentCableLengthRight)
                continue

                

