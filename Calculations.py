from tkinter import filedialog
from math import pi

RADIUS = 4

class DataProccessing():

    splitData = []

    def __init__(self):

        Circumference = 2*pi*RADIUS
        

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
            
