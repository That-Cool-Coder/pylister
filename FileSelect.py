import tkinter as tk
import tkinter.filedialog

class FileSelect(tk.Frame):
    # This is a class for a file selection widget,
    #  similar to html <input type="file">
    # It includes a label that shows the currently selected file,
    # And a button to select file

    # Access the current file using fileSelectObj.fileName
    # If no file is selected, then fileSelectObj.fileName is None

    def __init__(self, master, buttonText='Choose file', buttonFont=('Helvetica', 12),
        noFileSelectedText='No file selected', labelFont=('Helvetica', 12),
        maxFileNameLength=30, onSelectCallback=None):

        # Run the tk frame init instead of calling super,
        # Because for some reason super to frame doesn't work
        tk.Frame.__init__(self, master)
        
        # Configure this to have two columns and one row
        self.columnconfigure(0, pad=3)
        self.columnconfigure(1, pad=3)

        self.rowconfigure(0, pad=3)

        # Initialise the file name and properties
        self.fileName = None
        self.maxFileNameLength = maxFileNameLength
        self.noFileSelectedText = noFileSelectedText

        self.onSelectCallback = onSelectCallback

        # Create a label to show the current file...
        # ...and set it to the initial value...
        # ...then place it on the left
        self.fileNameLabel = tk.Label(self, font=labelFont)
        self.updateFileNameLabel()
        self.fileNameLabel.grid(row=0, column=0)

        # Create a button to change the selected file..
        # ...then place it on the right
        self.selectButton = tk.Button(self, text=buttonText, font=buttonFont,
            command=self.askFileName)
        self.selectButton.grid(row=0, column=1)

    def deselectFile(self):
        self.fileName = None
        self.updateFileNameLabel()
        
    def askFileName(self):
        # Open a file dialog and if the user selected something...
        # ...then make a callback

        self.fileName = tk.filedialog.askopenfilename()
        if self.fileName == ():
            self.fileName = None
        self.updateFileNameLabel()

        if self.fileName is not None:

            if self.onSelectCallback is not None:
                self.onSelectCallback()

    def updateFileNameLabel(self):
        # If a file is selected:
        if self.fileName is not None:
            # If the file name is short enough, then just write it on
            if len(self.fileName) <= self.maxFileNameLength:
                self.fileNameLabel.config(text=self.fileName)
            # Otherwise, trim it and put ... at the start
            else:
                # This is negative because we need to do n chars from the end
                # And there is a -3 because of the ...
                startIndex = -(self.maxFileNameLength) - 3
                shortenedFileName = '...' + self.fileName[startIndex:]
                self.fileNameLabel.config(text=shortenedFileName)
        # If no file is selected, then display the default text
        else:
            self.fileNameLabel.config(text=self.noFileSelectedText)
