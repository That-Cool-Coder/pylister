import tkinter as tk
import simpleFileManager as files

class PropertySelectMenu:

    def __init__(self, master, MAIN_FONT, propertyNameList,
        crntlySelectedProperties, saveCallback):
        self.master = master
        self.MAIN_FONT = MAIN_FONT
        self.propertyNameList = propertyNameList
        self.saveCallback = saveCallback

        self.window = tk.Toplevel(self.master)
        self.window.grab_set()

        self.heading = tk.Label(self.window, text='PyLister properties',
            font = self.MAIN_FONT)
        self.heading.pack(pady=30)

        self.createPropertyCheckboxes(crntlySelectedProperties)

        self.saveButton = tk.Button(self.window, text='Save',
            font=self.MAIN_FONT, command=self.saveSelectedProperties)
        self.saveButton.pack(pady=30)
    
    def createPropertyCheckboxes(self, crntlySelectedProperties):
        self.checkboxValues = []
        for prop in self.propertyNameList:
            var = tk.IntVar()
            self.checkboxValues.append(var)
            checkbox = tk.Checkbutton(self.window, text=prop, font=self.MAIN_FONT,
                variable=var)
            if prop in crntlySelectedProperties:
                checkbox.select()
            checkbox.pack()
        
    def saveSelectedProperties(self):
        propertyList = []
        for idx, value in enumerate(self.checkboxValues):
            if value.get() == 1:
                propertyList.append(self.propertyNameList[idx])
        self.saveCallback(propertyList)
        self.window.destroy()

    def mainloop(self):
        self.window.mainloop()