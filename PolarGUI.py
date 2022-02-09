import tkinter as tk
import threading
from tkinter.constants import DISABLED
from types import LambdaType
from PolarProjectMotors import StepperMotor
from Gondola import Gondola
from Calculations import DataProccessing



class App:
    def __init__(self, root):
        self.leftStepper = StepperMotor(15, 18, 23, 24)
        self.rightStepper = StepperMotor(25, 8, 12, 16)
        self.gondola = Gondola(7)
        self.proccessData = DataProccessing

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
        self.btnOpenFile=tk.Button(root, text="Open file", command=self.openFile) 
        self.btnOpenFile.place(x=700,y=470,width=70,height=25)


        #execute loaded project button
        self.btnExecute=tk.Button(root, text="Execute", command=self.execute) 
        self.btnExecute.place(x=300,y=270,width=60,height=60)


        #servo test button down
        self.btnExecute=tk.Button(root, text="ServoTestDown", command=self.ServoTestDown) 
        self.btnExecute.place(x=400,y=300,width=60,height=60)

        #servo test button down
        self.btnExecute=tk.Button(root, text="ServoTestUp", command=self.ServoTestUp) 
        self.btnExecute.place(x=470,y=350,width=60,height=60)


        #button stoping motors
        self.btnStopMotors=tk.Button(root, text="Stop", command=self.stopMotors) 
        self.btnStopMotors.place(x=200,y=150,width=60,height=60)


    #testing servo down
    def ServoTestDown(self):
        self.gondola.penDown()
    #testing servo up


    def ServoTestUp(self):
        self.gondola.penUp()


    #function opening files to read
    def openFile(self):
            self.proccessData.loadData(self)


    # buttong stopping execution
    def stopMotors(self):
        self.rightStepper.stopMotors()
        self.enableButtons()


    #function disable buttons
    def disableButtons(self):
        self.btnExecute['state'] = 'disabled'
        self.btnOpenFile['state'] = 'disabled'


        #function enable buttons
    def enableButtons(self):
        self.btnExecute['state'] = 'normal'
        self.btnOpenFile['state'] = 'normal'


    #function calling in execution of stepper 
    #motors in parralel
    def stepperMotorsCall(self,lDirection,lNoofSteps,lSpeed,rdirection,rNoOfSteps,rSpeed):

        if (self.rightStepper.stopMotor == False):

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
    def execute(self):

        #changing status of motors - bool true
        self.rightStepper.startMotors()  

        executeSampleThreadLambda = lambda:(
            self.disableButtons(),
            self.stepperMotorsCall("left", 150,2, "left", 400,1),
            self.stepperMotorsCall("left", 50,1, "right", 200,3),
            self.stepperMotorsCall("right", 500,1, "right", 500,6),
            self.stepperMotorsCall("left", 500,10, "left", 500,0),
            self.stepperMotorsCall("right", 500,1, "right", 100,6),
            self.stepperMotorsCall("right", 400,12, "right", 200,0),
            self.stepperMotorsCall("left", 500,1, "left", 500,1),
            self.stepperMotorsCall("right", 400,1, "left", 200,2),
            self.stepperMotorsCall("left", 200,1, "right", 600,1.2),
            self.enableButtons())

        executeSampleThread = threading.Thread(target = executeSampleThreadLambda, daemon=True)
        executeSampleThread.start()



#main menu
if __name__ == "__main__":

    root = tk.Tk()
    app = App(root)
    root.mainloop()