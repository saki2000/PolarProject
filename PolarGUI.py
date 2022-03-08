import threading
import tkinter as tk
from tkinter.constants import DISABLED
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
        self.btnExecute=tk.Button(root, text="Execute", command=self.executeDrawing) 
        self.btnExecute.place(x=300,y=270,width=60,height=60)


        #servo test button down
        self.btnServoDown=tk.Button(root, text="servoDown", command=self.servoDown) 
        self.btnServoDown.place(x=400,y=300,width=60,height=60)

        #servo test button down
        self.btnServoUp=tk.Button(root, text="servoUp", command=self.servoUp) 
        self.btnServoUp.place(x=470,y=350,width=60,height=60)


        #button stoping motors
        self.btnStopMotors=tk.Button(root, text="Stop", command=self.stopMotors) 
        self.btnStopMotors.place(x=200,y=150,width=60,height=60)


    #testing servo down
    def servoDown(self):
        self.gondola.penDown()
    #testing servo up


    def servoUp(self):
        self.gondola.penUp()


    #function opening files to read
    def openFile(self):
        self.proccessData.loadData()


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



