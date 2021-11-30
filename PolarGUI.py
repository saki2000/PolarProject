import tkinter as tk
import threading
from tkinter import filedialog
from tkinter.constants import DISABLED
from types import LambdaType
from PolarProjectMotors import StepperMotor

class App:
    def __init__(self, root):
        self.leftStepper = StepperMotor(15, 18, 23, 24)
        self.rightStepper = StepperMotor(25, 8, 12, 16)

        #setting title
        root.title("Polar Project")
        #setting window size
        width=841
        height=562
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        #open hpgl file button
        btnOpenFile=tk.Button(root, text="Open file", command=self.openFile) 
        btnOpenFile.place(x=700,y=470,width=70,height=25)

        #execute loaded project button
        self.btnExecute=tk.Button(root, text="Execute", command=self.sample) 
        self.btnExecute.place(x=300,y=270,width=60,height=60)

        #function opening files to read
    def openFile(self):
        self.dataFile = filedialog.askopenfilename(filetypes=(("HPGL Files", "*.hpgl"),))
        self.dataFile = open(self.dataFile, 'r')
        DATAPOINTS = self.dataFile.read()
        self.dataFile.close()

        #function disable buttons
    def disableButtons(self):
        self.btnExecute['state'] = 'disabled'
        self.dataFile['state'] = 'disabled'

        #function enable buttons
    def enableButtons(self):
        self.btnExecute['state'] = 'normal'
        self.btnExecute['state'] = 'normal'


    #function calling in execution of stepper 
    #motors in parralel
    def stepperMotorsCall(self,lDirection,lNoofSteps,lSpeed,rdirection,rNoOfSteps,rSpeed):

        #creating threads for each stepper
        leftStepperThread = threading.Thread(target  = self.leftStepper.stepperControl, args=[lDirection,lNoofSteps,lSpeed], daemon = True )
        rightStepperThread = threading.Thread(target = self.rightStepper.stepperControl, args=[rdirection,rNoOfSteps,rSpeed], daemon = True)

        leftStepperThread.start()
        rightStepperThread.start()

        #joining threads
        leftStepperThread.join()
        rightStepperThread.join()
    
    #lambda function spawning a new dameon thread that will spawn 
    #threads and execute stepper motor calls
    def sample(self):
        executeSampleThreadLambda = lambda:(
            self.disableButtons(),
            self.stepperMotorsCall("left", 150,0.001, "left", 400,0),
            self.stepperMotorsCall("left", 50,0, "right", 200,0.0005),
            self.stepperMotorsCall("right", 500,0, "right", 500,0.005),
            self.stepperMotorsCall("left", 500,0.005, "left", 500,0),
            self.stepperMotorsCall("right", 500,0, "right", 100,0.0005),
            self.stepperMotorsCall("right", 400,0.0007, "right", 200,0),
            self.stepperMotorsCall("left", 500,0.0001, "left", 500,0),
            self.stepperMotorsCall("right", 400,0, "left", 200,0.0001),
            self.stepperMotorsCall("left", 200,0, "right", 600,0.0005),
            self.enableButtons())

        executeSampleThread = threading.Thread(target = executeSampleThreadLambda, daemon=True)
        executeSampleThread.start()
    

#main menu
if __name__ == "__main__":

    root = tk.Tk()
    app = App(root)
    root.mainloop()