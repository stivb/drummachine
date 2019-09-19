from Tkinter import *

#next integrate this into menus
class BarCopier:

    def __init__(self, parent, parentself):

        top = self.top = Toplevel(parent)
        self.parent = parentself

        mainframe = Frame(top)
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)
        mainframe.pack(pady=100, padx=100)

        self.barfrom = StringVar(top)
        self.barto = StringVar(top)
        self.barinsert = StringVar(top)

        numbers = []
        for x in range(1, 256):
            numbers.append(str(x))

        Label(mainframe, text="Copy From Bar").grid(row=1, column=1)
        fromBarDropDown = OptionMenu(mainframe, self.barfrom, *numbers)
        fromBarDropDown.grid(row=2, column=1)
        Label(mainframe, text="Copy to Bar").grid(row=1, column=3)
        toBarDropDown = OptionMenu(mainframe, self.barto, *numbers)
        toBarDropDown.grid(row=2, column=3)
        Label(mainframe, text="Insert At Bar").grid(row=1, column=5)
        insertAtBarDropDown = OptionMenu(mainframe, self.barinsert, *numbers)
        insertAtBarDropDown.grid(row=2, column=5)


        self.T = Text(mainframe,height=1,width=30)
        self.T.grid(row=4,column=1,columnspan=5)

        cmdbtn = Button(mainframe, text="Check", command=self.trycommand)
        cmdbtn.grid(row=4,column=6)

        okbtn = Button(mainframe, text="OK", command=self.okcommand)
        okbtn.grid(row=6,column=2)
        cancelbtn = Button(mainframe, text="cancel", command=self.cancelcommand)
        cancelbtn.grid(row=6,column=4)

    def trycommand(self):
        self.T.insert(END, self.barfrom.get() + " to " + self.barto.get() + " at " + self.barinsert.get())

    def okcommand(self):
        self.parent.duplicateSequentialBars(int(self.barfrom.get()),int(self.barto.get()),int(self.barinsert.get()))

    def cancelcommand(self):
        self.T.insert(END,self.barfrom.get() + " to " + self.barto.get() + " at "+ self.barinsert.get())


    def ok(self):

        self.top.destroy()




def showBarCopier():
    d = BarCopier(root)

