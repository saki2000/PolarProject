import tkinter as tk
from tkinter import filedialog
from PolarProjectMotors import *





#function opening files to read
def openFile():
    dataFile = filedialog.askopenfilename(filetypes=(("HPGL Files", "*.hpgl"),))
    dataFile = open(dataFile, 'r')
    DATAPOINTS = dataFile.read()
    dataFile.close()




class App:
    def __init__(self, root):
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
        btnOpenFile=tk.Button(root, text="Open file", command=openFile) 
        btnOpenFile.place(x=700,y=470,width=70,height=25)

        #execute loaded project button
        btnExecute=tk.Button(root, text="Execute", command=sample) 
        btnExecute.place(x=300,y=270,width=60,height=60)

    

#main menu
if __name__ == "__main__":

    root = tk.Tk()
    app = App(root)
    root.mainloop()