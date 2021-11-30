import tkinter as tk
from tkinter import filedialog

#function opening files to read
def openFile():
    dataFile = filedialog.askopenfilename(filetypes=(("HPGI Files", "*.hpgi"),))
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

        btnOpenFile=tk.Button(root, text="Open file", command=openFile) 
        btnOpenFile.place(x=700,y=470,width=70,height=25)

 

    def btnOpenFile_command(self):
        print("command")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()