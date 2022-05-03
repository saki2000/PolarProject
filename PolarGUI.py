import threading
import tkinter as tk
from tkinter.constants import DISABLED
from tkinter import Label, Scale, messagebox
from types import LambdaType
from Gondola import Gondola
from PointsProccessing import DataProccessing



class App:
    def __init__(self, root):
        self.gondola = Gondola(7)
        self.proccessData = DataProccessing()

        #setting title
        root.title("Polar Project")
        #setting window size
        width=800
        height=600
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)


        #exit button
        self.btnExit=tk.Button(root, text="EXIT", command=self.closeAPP) 
        self.btnExit.place(x=700,y=500,width=80,height=80)
      

        #Move Gondola Up button
        self.btnGondolaUp=tk.Button(root, text="Up") 
        self.btnGondolaUp.place(x=110,y=20,width=60,height=80)


        #Move Gondola down button
        self.btnGondolaDown=tk.Button(root, text="Down") 
        self.btnGondolaDown.place(x=110,y=140,width=60,height=80)


        #Move Gondola left button
        self.btnGondolaLeft=tk.Button(root, text="Left") 
        self.btnGondolaLeft.place(x=20,y=80,width=80,height=60)


        #Move Gondola Right button
        self.btnGondolaRight=tk.Button(root, text="Right") 
        self.btnGondolaRight.place(x=180,y=80,width=80,height=60)


        #pen Up button
        self.btnServoDown=tk.Button(root, text="Pen Up", command=self.servoUp) 
        self.btnServoDown.place(x=300,y=40,width=80,height=80)


        #pen Down button
        self.btnServoUp=tk.Button(root, text="Pen Down", command=self.servoDown) 
        self.btnServoUp.place(x=300,y=160,width=80,height=80)

        #execute loaded project button
        self.btnExecute=tk.Button(root, text="Execute", command=self.executeDrawing) 
        self.btnExecute.place(x=40,y=420,width=100,height=100)


        #button stoping motors
        self.btnStopMotors=tk.Button(root, text="Stop", command=self.stopMotors) 
        self.btnStopMotors.place(x=180,y=440,width=80,height=80)


        #open hpgl file button
        self.btnOpenFile=tk.Button(root, text="Open file", command=self.openFile) 
        self.btnOpenFile.place(x=650,y=40,width=120,height=40)


        #updates scale sieze in calculation object
        self.btnSetScale=tk.Button(root, text="Set", command=self.scaleAdjustment) 
        self.btnSetScale.place(x=530,y=130,width=60,height=60)

        #btnResetingStart position
        self.btnResetStartPosition=tk.Button(root, text="Reset Start", command=self.resetStart) 
        self.btnResetStartPosition.place(x=100,y=300,width=80,height=50)


        #slider for adjusting scale size
        self.scaleSlider = Scale(root, from_ = 100, to = -100, length = 200, resolution = 0.1)
        self.scaleSlider.place(x = 450, y = 60)


        #Scale label information
        self.lblScale = Label(root, text = "Current Scale Set: " + str(self.proccessData.positionCalculation.scale) + "%")
        self.lblScale.place(x = 430, y = 280)

    
    #Closing application
    def closeAPP(self):
        result = messagebox.askyesno(title = "Exit Program", message= "Would You Like To Exit ?")
        if result :
            root.quit()


    #checking for boundries 
    def checkAllowedPosition(self, positionToCheck):
        
        if(positionToCheck < 0):
            return 0
        
        if(positionToCheck > self.proccessData.positionCalculation.STEPPER_MOTOR_DISTANCE):
            return self.proccessData.positionCalculation.STEPPER_MOTOR_DISTANCE
        
        return positionToCheck
            

    #moving gondola up by 10 points
    def movePenUp(self):
        
        newPositionX = self.proccessData.positionCalculation.currentPositionX
        newPositionY = self.checkAllowedPosition(self.proccessData.positionCalculation.currentPositionY - 100)

        directionLeft, numberOfStepsLeftMotor, leftRatio, directionRight, numberOfStepsRightMotor, rightRatio = self.proccessData.positionCalculation.getMotorsData(newPositionX, newPositionY)


    #moving gondola down by 10 points
    def movePenDown(self):
        
        newPositionX = self.proccessData.positionCalculation.currentPositionX
        newPositionY = self.checkAllowedPosition(self.proccessData.positionCalculation.currentPositionY + 100)

        directionLeft, numberOfStepsLeftMotor, leftRatio, directionRight, numberOfStepsRightMotor, rightRatio = self.proccessData.positionCalculation.getMotorsData(newPositionX, newPositionY)
        self.proccessData.stepperMotorsCall(directionLeft, numberOfStepsLeftMotor, leftRatio, directionRight, numberOfStepsRightMotor, rightRatio)

    #moving gondola left by 10 points
    def movePenLeft(self):
        newPositionX = self.checkAllowedPosition(self.proccessData.positionCalculation.currentPositionY - 100)
        newPositionY = self.proccessData.positionCalculation.currentPositionY

        directionLeft, numberOfStepsLeftMotor, leftRatio, directionRight, numberOfStepsRightMotor, rightRatio = self.proccessData.positionCalculation.getMotorsData(newPositionX, newPositionY)
        self.proccessData.stepperMotorsCall(directionLeft, numberOfStepsLeftMotor, leftRatio, directionRight, numberOfStepsRightMotor, rightRatio)


    #moving gondola right by 10 points
    def movePenRight(self):
        newPositionX = self.checkAllowedPosition(self.proccessData.positionCalculation.currentPositionY + 100)
        newPositionY = self.proccessData.positionCalculation.currentPositionY

        directionLeft, numberOfStepsLeftMotor, leftRatio, directionRight, numberOfStepsRightMotor, rightRatio = self.proccessData.positionCalculation.getMotorsData(newPositionX, newPositionY)
        self.proccessData.stepperMotorsCall(directionLeft, numberOfStepsLeftMotor, leftRatio, directionRight, numberOfStepsRightMotor, rightRatio)

    


    #setting servo position down
    def servoDown(self):
        self.gondola.penDown()


    #setting servo position up
    def servoUp(self):
        self.gondola.penUp()


    #function opening files to read
    def openFile(self):
        self.proccessData.loadData()


    # buttong stopping execution
    def stopMotors(self):
        self.proccessData.rightStepper.stopMotors()
        self.enableButtons()

    
    #updading scale button
    def scaleAdjustment(self):

        newScale = self.scaleSlider.get()
        if newScale == 0:
            newScale = 1
        if newScale < 0:
            newScale = abs(newScale) / 100 

        self.proccessData.positionCalculation.scale = newScale / 100

        if newScale < 1:
            newScaleToPrint = 100 - (newScale * 100)
        else:
            newScaleToPrint = newScale * 100

        #updating label.
        self.lblScale.destroy()
        self.lblScale = Label(root, text = "Current Scale Set: " + str(newScaleToPrint) + "%")
        self.lblScale.place(x = 430, y = 280)
        

    #function disable buttons
    def disableButtons(self):
        self.btnExecute['state'] = 'disabled'
        self.btnOpenFile['state'] = 'disabled'
        self.btnGondolaDown['state'] = 'disabled'
        self.btnGondolaLeft['state'] = 'disabled'
        self.btnGondolaRight['state'] = 'disabled'
        self.btnGondolaUp['state'] = 'disabled'
        self.btnServoDown['state'] = 'disabled'
        self.btnServoUp['state'] = 'disabled'


        #function enable buttons
    def enableButtons(self):
        self.btnExecute['state'] = 'normal'
        self.btnOpenFile['state'] = 'normal'
        self.btnGondolaDown['state'] = 'normal'
        self.btnGondolaLeft['state'] = 'normal'
        self.btnGondolaRight['state'] = 'normal'
        self.btnGondolaUp['state'] = 'normal'
        self.btnServoDown['state'] = 'normal'
        self.btnServoUp['state'] = 'normal'


    #reseting start position
    def resetStart(self):
        self.proccessData.positionCalculation.resetStartPosition()


        #function executing drawing
        #this function spawn deamon thread that then can spawn additional
        #threads to execute individual steps
    def executeDrawing(self):

        self.disableButtons()

        exacuteLambdaThread = lambda:(
            self.proccessData.executeFile(),
            self.enableButtons()
        )

        exacuteThread = threading.Thread(target = exacuteLambdaThread, daemon=True)
        exacuteThread.start()
    


#main menu
if __name__ == "__main__":

    root = tk.Tk()
    app = App(root)
    root.mainloop()



