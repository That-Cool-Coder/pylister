import tkinter as tk
import tkinter.messagebox
import os.path

from FileSelect import *
import simpleFileManager as files

from lister import *

class Application:
    
    # Some UI presets
    TITLE_FONT = ('Helvetica', 35)
    MAIN_FONT = ('Helvetica', 12)
    ICON_PATH = 'icon.png'
    INIT_SIZE = '500x600'

    # A collection of analysis functions to call
    # The key for each pair is the label to output and...
    # ...the value is the function to call
    PROPERTIES_TO_ANALYSE = {
        'Total lines' : countLines,
        'Lines of code' : countCodeLines,
        'Comment lines' : countCommentLines,
        'Blank lines' : countBlankLines,

        'Assignment statements' : countAssignments,
        'Classes' : countClasses,
        'Functions' : countFunctions,
        'Branch statements' : countBranches,
        'Loops' : countLoops,
        'Try-except blocks' : countTryExcepts
    }

    def __init__(self, master):
        self.master = master
        self.master.title('PyLister')
        self.master.geometry(self.INIT_SIZE)

        # Set the image icon for the photo
        self.master.iconphoto(True, tk.PhotoImage(file=self.ICON_PATH))

        # Create heading for UI
        self.title = tk.Label(self.master, text='PyLister', font=self.TITLE_FONT)
        self.title.pack()

        # Create a file selector for the file to analyse
        self.fileSelect = FileSelect(self.master, buttonFont=self.MAIN_FONT,
            labelFont=self.MAIN_FONT, noFileSelectedText='Select a file to analyse')
        self.fileSelect.pack(pady=30)

        # Create a button to do the analysis
        self.analyseButton = tk.Button(self.master,
            text='Analyse file', font=self.MAIN_FONT, command=self.analyseFile)
        self.analyseButton.pack(pady=0)

        # Create a place to display the results in
        self.resultsFrame = tk.Frame(self.master, background='white')
        self.resultsFrame.pack(pady=30, padx=30, fill=tk.BOTH, expand=True, side=tk.LEFT)

    def analyseFile(self):
        fileName = self.fileSelect.fileName
        # If no file is selected, give a warning
        if fileName is None:
            tk.messagebox.showwarning(message='Please select a file')
            return
        try:
            # Remove all children of output frame
            for widget in self.resultsFrame.winfo_children():
                widget.destroy()
            
            # Loop through all of the things to analyse
            analysis = {}
            codeToAnalyse = files.read(fileName)
            for value in self.PROPERTIES_TO_ANALYSE:
                analysis[value] = self.PROPERTIES_TO_ANALYSE[value](code=codeToAnalyse)

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
            self.fileSelect.deselectFile()
            return

        except:
            tk.messagebox.showerror('Unknown error', 'An unexpected error has occured')
            return
    
    def displayAnalysis(self, analysis):
        # Get the name and extension of the selected file
        fileName = os.path.basename(self.fileSelect.fileName)

        # Create a heading for the results
        self.resultsHeading = tk.Label(self.resultsFrame, font=self.MAIN_FONT,
            text=f'Analysis of {fileName}:', background='white')
        self.resultsHeading.pack(pady=10)

        # Loop through the results and create a label to display each one
        for value in analysis:
            text = f'{value}: {analysis[value]}'
            label = tk.Label(self.resultsFrame, text=text, font=self.MAIN_FONT, background='white')
            label.pack(padx=10, pady=5)


    def mainloop(self):
        self.master.mainloop()

if __name__ == '__main__':
    application = Application(tk.Tk())
    application.mainloop()