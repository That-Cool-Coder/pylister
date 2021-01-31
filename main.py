import tkinter as tk
import tkinter.messagebox

from FileSelect import *
import simpleFileManager as files

from lister import *

class Application:
    titleFont = ('Helvetica', 35)
    mainFont = ('Helvetica', 10)
    initSize = '500x600'

    propertiesToAnalyse = {
        'functions' : countFunctions,
        'lines' : countLines
    }

    def __init__(self, master):
        self.master = master
        self.master.title('PyLister')
        self.master.iconphoto(True, tk.PhotoImage(file='icon.png'))

        self.master.geometry(self.initSize)

        self.title = tk.Label(self.master, text='PyLister', font=self.titleFont)
        self.title.pack()

        self.fileSelect = FileSelect(self.master, buttonFont=self.mainFont,
            labelFont=self.mainFont, noFileSelectedText='Select a file to analyse')
        self.fileSelect.pack(pady=30)

        self.analyseButton = tk.Button(self.master,
            text='Analyse file', font=self.mainFont, command=self.analyseFile)
        self.analyseButton.pack(pady=0)

        self.outputFrame = tk.Frame(self.master)
        self.outputFrame.pack(pady=30)

    def analyseFile(self):
        fileName = self.fileSelect.fileName
        if fileName is None:
            tk.messagebox.showwarning(message='Please select a file')
            return
        try:
            # Remove all children of output frame
            for widget in self.outputFrame.winfo_children():
                widget.destroy()

            analysis = {}

            codeToAnalyse = files.read(fileName)

            for value in self.propertiesToAnalyse:
                analysis[value] = self.propertiesToAnalyse[value](code=codeToAnalyse)

            self.displayAnalysis(analysis)

        except PermissionError:
            tk.messagebox.showerror('Permission error',
                'You do not have the permissions to view this file')
        
        except FileNotFoundError:
            tk.messagebox.showerror('File not found error',
                'The file you are looking for does not exist')

        except:
            tk.messagebox.showerror('Unknown error', 'An unexpected error has occured')
            raise 
            return
    
    def displayAnalysis(self, analysis):
        for value in analysis:
            text = f'{value}: {analysis[value]}'
            label = tk.Label(self.outputFrame, text=text, font=self.mainFont)
            label.pack(side=tk.LEFT)


    def mainloop(self):
        self.master.mainloop()

if __name__ == '__main__':
    application = Application(tk.Tk())
    application.mainloop()