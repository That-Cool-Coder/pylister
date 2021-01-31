import tkinter as tk
import tkinter.filedialog

class FileSelect(tk.Frame):
    def __init__(self, master, buttonText='Choose file', buttonFont=('Helvetica', 12),
        noFileSelectedText='No file selected', labelFont=('Helvetica', 12),
        maxFileNameLength=30, onSelectCallback=None):

        tk.Frame.__init__(self, master)
        
        self.columnconfigure(0, pad=3)
        self.columnconfigure(1, pad=3)

        self.rowconfigure(0, pad=3)

        self.fileName = None
        self.maxFileNameLength = maxFileNameLength
        self.noFileSelectedText = noFileSelectedText

        self.onSelectCallback = onSelectCallback

        self.fileNameLabel = tk.Label(self, font=labelFont)
        self.updateFileNameLabel()
        self.fileNameLabel.grid(row=0, column=0)

        self.selectButton = tk.Button(self, text=buttonText, font=buttonFont,
            command=self.askFileName)
        self.selectButton.grid(row=0, column=1)
        
    def askFileName(self):
        self.fileName = tk.filedialog.askopenfilename()
        self.updateFileNameLabel()

        if self.onSelectCallback is not None:
            self.onSelectCallback()

    def updateFileNameLabel(self):
        print('File name is:', self.fileName)
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
        else:
            self.fileNameLabel.config(text=self.noFileSelectedText)
