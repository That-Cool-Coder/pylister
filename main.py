import tkinter as tk
import tkinter.messagebox
import os.path

from PropertySelectMenu import PropertySelectMenu
from FileSelect import *
import simpleFileManager as files

from lister import *

class Application:
    
    # Some UI presets
    TITLE_FONT = ('Helvetica', 35)
    MAIN_FONT = ('Helvetica', 12)
    ICON_PATH = 'icon.png'
    INIT_SIZE = '500x600'

    # A collection of analysis functions that can be called
    # The key for each pair is the label to output and...
    # ...the value is the function to call
    PROPERTIES_TO_ANALYSE = {
        'total lines' : countLines,
        'lines of code' : countCodeLines,
        'comment lines' : countCommentLines,
        'blank lines' : countBlankLines,

        'assignment statements' : countAssignments,
        'classes' : countClasses,
        'functions' : countFunctions,
        'branch statements' : countBranches,
        'loops' : countLoops,
        'try-except blocks' : countTryExcepts
    }

    def __init__(self):
        self.window = tk.Tk()
        self.window.title('PyLister')
        self.window.geometry(self.INIT_SIZE)

        self.crntPropertyList = self.PROPERTIES_TO_ANALYSE.keys()

        # Set the image icon for the photo
        self.window.iconphoto(True, tk.PhotoImage(file=self.ICON_PATH))

        # Create heading for UI
        self.title = tk.Label(self.window, text='PyLister', font=self.TITLE_FONT)
        self.title.pack()

        # Create a file selector for the file to analyse
        self.fileSelect = FileSelect(self.window, buttonFont=self.MAIN_FONT,
            labelFont=self.MAIN_FONT, noFileSelectedText='Select a file to analyse')
        self.fileSelect.pack(pady=30)

        # Create a button to do the analysis
        self.analyseButton = tk.Button(self.window,
            text='Analyse file', font=self.MAIN_FONT, command=self.analyseFile)
        self.analyseButton.pack(pady=0)

        self.PropertyListButton = tk.Button(self.window,
            text='Change Property List', font=self.MAIN_FONT, command=self.openPropertySelectMenu)
        self.PropertyListButton.pack()

        scrollbar = tk.Scrollbar(self.window, orient='vertical')
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create a place to display the results in
        self.resultsFrame = tk.Frame(self.window, background='white')
        self.resultsFrame.pack(pady=30, padx=30, fill=tk.BOTH, expand=True, side=tk.LEFT)

        self.resultsText = tk.Text(self.resultsFrame, background='white',
            yscrollcommand=scrollbar.set, font=self.MAIN_FONT, bd=0)
        self.resultsText.config(highlightthickness=0)
        self.resultsText.tag_configure('center', justify='center')
        self.resultsText.pack()

        scrollbar.config(command=self.resultsText.yview)

    def analyseFile(self):
        fileName = self.fileSelect.fileName
        # If no file is selected, give a warning
        if fileName is None:
            tk.messagebox.showwarning(message='Please select a file')
            return
        try:
            # Loop through all of the things to analyse
            analysis = {}
            codeToAnalyse = files.read(fileName)
            for value in self.crntPropertyList:
                func = self.PROPERTIES_TO_ANALYSE[value]
                analysis[value] = func(code=codeToAnalyse)

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
            raise
            return
    
    def displayAnalysis(self, analysis):
        # Get the name and extension of the selected file
        fileName = os.path.basename(self.fileSelect.fileName)

        self.resultsText.delete(1.0, tk.END)

        # Create a heading for the results
        self.resultsText.insert(tk.END,
            f'\nAnalysis of {fileName}:\n\n', 'center')

        # Loop through the results and create a label to display each one
        for value in analysis:
            text = f'{value}: {analysis[value]}\n\n'
            self.resultsText.insert(tk.END, text, 'center')

    def openPropertySelectMenu(self):
        propertySelectMenu = PropertySelectMenu(self.window, self.MAIN_FONT,
            list(self.PROPERTIES_TO_ANALYSE.keys()), self.crntPropertyList,
            self.updatePropertyList)
        propertySelectMenu.mainloop()
    
    def updatePropertyList(self, propertyList):
        self.crntPropertyList = propertyList

    def mainloop(self):
        self.window.mainloop()


if __name__ == '__main__':
    application = Application()
    application.mainloop()