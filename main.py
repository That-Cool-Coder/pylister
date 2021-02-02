import tkinter as tk
import tkinter.messagebox
import os.path

from FileSelect import *
import simpleFileManager as files

from lister import *

class Application:
    titleFont = ('Helvetica', 35)
    mainFont = ('Helvetica', 12)
    initSize = '500x600'

    propertiesToAnalyse = {
        'total lines' : countLines,
        'lines of code' : countCodeLines,
        'comment lines' : countCommentLines,
        'blank lines' : countBlankLines,

        'classes' : countClasses,
        'functions' : countFunctions,
        'branch statements' : countBranches,
        'loops' : countLoops,
        'Try-except statements' : countTryExcepts
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

        self.outputFrame = tk.Frame(self.master, background='white')
        self.outputFrame.pack(pady=30, padx=30, fill=tk.BOTH, expand=True, side=tk.LEFT)

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
            return
        
        except FileNotFoundError:
            tk.messagebox.showerror('File not found error',
                'The file you are looking for does not exist')
            return
        
        except UnicodeError:
            tk.messagebox.showerror('Unicode error',
                'This file can not be read as python code')

        except:
            tk.messagebox.showerror('Unknown error', 'An unexpected error has occured')
            raise 
            return
    
    def displayAnalysis(self, analysis):
        fileName = os.path.basename(self.fileSelect.fileName)
        self.resultsHeading = tk.Label(self.outputFrame, font=self.mainFont,
            text=f'Analysis of {fileName}:', background='white')
        self.resultsHeading.pack(pady=10)

        for value in analysis:
            text = f'{value}: {analysis[value]}'
            label = tk.Label(self.outputFrame, text=text, font=self.mainFont, background='white')
            label.pack(padx=10, pady=5)


    def mainloop(self):
        self.master.mainloop()

if __name__ == '__main__':
    application = Application(tk.Tk())
    application.mainloop()