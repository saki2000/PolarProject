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
        
    

    #lambda function spawning a new dameon thread that will spawn 
    #threads and execute stepper motor calls
    def stepExecute(self,directionLeft, numberOfStepsLeftMotor, leftRatio, directionRight, numberOfStepsRightMotor, rightRatio):

        #changing status of motors - bool true
        self.rightStepper.startMotors()  

        executeLambdaThred = lambda:(

            self.stepperMotorsCall(directionLeft, numberOfStepsLeftMotor, leftRatio, directionRight, numberOfStepsRightMotor, rightRatio),)

        executeSampleThread = threading.Thread(target = executeLambdaThred, daemon=True)
        executeSampleThread.start()









        


    #interpreting all commands for loaded list - splitData

    def commands(self):

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
                time.sleep(0.5)
                positions  = self.splitData[num][2:]
                positionsList = positions.split(',')
                
                #prevents crash when command has no parameters
                if (len(positionsList) == 0 or len(positionsList) == 1):
                    continue


                for n in range (0,len(positionsList),2):

                    #prevents division by zero
                    if(positionsList[n] == "0" and positionsList[n+1] == "0"):
                        continue

                    else:
                        print( positionsList[n], positionsList[n+1])
                        directionLeft, numberOfStepsLeftMotor, leftRatio, directionRight, numberOfStepsRightMotor, rightRatio = self.positionCalculation.stepperMotorsData(int(positionsList[n]), int(positionsList[n+1]))
                        self.stepExecute(directionLeft, numberOfStepsLeftMotor, leftRatio, directionRight, numberOfStepsRightMotor, rightRatio)
                   
                continue

            #Pen down
            #Draw following position in command list

            elif command == "PD":
                self.gondola.penDown()
                time.sleep(0.5)
                positions  = self.splitData[num][2:]
                positionsList = positions.split(',')
                
                #prevents crash when command has no parameters
                if (len(positionsList) == 0 or len(positionsList) == 1):
                    continue
                
                for n in range (0,len(positionsList),2):

                    #prevents division by zero
                    if(positionsList[n] == "0" and positionsList[n+1] == "0"):
                        continue

                    print(positionsList[n], positionsList[n+1])
                    directionLeft, numberOfStepsLeftMotor, leftRatio, directionRight, numberOfStepsRightMotor, rightRatio = self.positionCalculation.stepperMotorsData(int(positionsList[n]), int(positionsList[n+1]))
                    self.stepExecute(directionLeft, numberOfStepsLeftMotor, leftRatio, directionRight, numberOfStepsRightMotor, rightRatio)
                continue

                

