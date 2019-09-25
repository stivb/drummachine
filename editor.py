import Tkinter
from Tkinter import *
from ScrolledText import *
import tkFileDialog
import tkMessageBox
import tkFont



# create a menu & define functions for each menu item

class Editor:

    def __init__(self,parentself):


        self.parent = parentself
        self.clmct = 0


    def open_command(self):
        file = tkFileDialog.askopenfile(parent=root, mode='rb', title='Select a file')
        if file != None:
            contents = file.read()
            self.textPad.insert('1.0', contents)
            file.close()


    def save_command(self):
        file = tkFileDialog.asksaveasfile(mode='w')
        if file != None:
            # slice off the last character from get, as an extra return is added
            data = self.textPad.get('1.0', END + '-1c')
            file.write(data)
            file.close()


    def exit_command(self):
        if tkMessageBox.askokcancel("Quit", "Do you really want to quit?"):
            self.top.destroy()


    def about_command(self):
        label = tkMessageBox.showinfo("About", "Just Another TextPad \n Copyright \n No rights left to reserve")


    def dummy(self):
        print "I am a Dummy Command, I will be removed in the next step"

    def rehearsePattern(self):
        self.parent.formula.set(self.getPatternInsertText())
        self.parent.play_in_thread_seq()


    def addPattern(self):

        self.textPad.insert(INSERT, self.getPatternInsertText())

    def getPatternInsertText(self):
        ptn = self.editorPttn.get() + " "
        transpose = "+" + self.transposeOffset.get()  + " "
        fromto = self.editorFrom.get() + "-" + self.editorTo.get()
        reps = "*" + self.Repetitions.get() + " "
        stringtoinsert = "{" + ptn + transpose + fromto + "}"+reps
        return stringtoinsert

    def saveText(self):
        self.parent.trackText.set(self.textPad.get(1.0,END))
        self.top.destroy()

    def addDrop(self):
        print self.dropPattern.get()

    def clm(self):
        self.clmct+=1
        return self.clmct

    def clm0(self):
        self.clmct=0

    def init_ui(self):

        self.top = Toplevel(self.parent.root)
        self.top.geometry('800x600')
        #self.top.grid_columnconfigure(0, weight=1, uniform="fred")
        self.editorPttn = StringVar()
        self.editorFrom = StringVar()
        self.editorTo = StringVar()
        self.transposeOffset = StringVar()
        self.Repetitions = StringVar()
        self.dropPattern = StringVar()

        label_font = tkFont.Font(family='Courer', size=25)

        Label(self.top, text="Pattern").grid(row=0, column=0, sticky=NW)
        self.editorPttn.set("1")
        self.editorPtnDropDown = OptionMenu(self.top, self.editorPttn, 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32)
        self.editorPtnDropDown.grid(row=0, column=self.clm(), sticky=NW)

        Label(self.top, text="From").grid(row=0, column=self.clm(),sticky=NW)
        self.editorFrom.set('1')  # set the default option
        editorFromDropDown = OptionMenu(self.top, self.editorFrom, 1,2,3,4,5,6,7,8)
        editorFromDropDown.grid(row=0, column=self.clm(), sticky=NW)

        Label(self.top, text="To").grid(row=0, column=self.clm(), sticky=NW)
        self.editorTo.set('32')  # set the default option
        editorToDropDown = OptionMenu(self.top, self.editorTo, 4, 8, 12, 16, 20, 24, 28, 32)
        editorToDropDown.grid(row=0, column=self.clm(),sticky=NW)

        Label(self.top, text="Transpose").grid(row=0, column=self.clm(),sticky=NW)
        self.transposeOffset.set('0')  # set the default option
        transposeOffsetDropDown = OptionMenu(self.top, self.transposeOffset, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
        transposeOffsetDropDown.grid(row=0, column=self.clm(), sticky=NW)

        Label(self.top, text="Repetitions").grid(row=0, column=self.clm(), sticky=NW)
        self.Repetitions.set('1')  # set the default option
        RepetitionsDropDown = OptionMenu(self.top, self.Repetitions, 1,2,3,4,5,6,7,8)
        RepetitionsDropDown.grid(row=0, column=self.clm(), sticky=NW)

        patternRehearseButton = Button(self.top, text="Preview", command=self.rehearsePattern)
        patternRehearseButton.grid(row=0, column=self.clm(), sticky=NW)

        patternHelperButton = Button(self.top, text="Add", command=self.addPattern)
        patternHelperButton.grid(row=0, column=self.clm(), sticky=NW)

        columnTotal = self.clm()

        Label(self.top, text="Drop Pattern").grid(row=1, column=self.clm0(), sticky=NW)
        self.dropPattern.set("1")
        self.dropPatternDropDown = OptionMenu(self.top, self.dropPattern, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,
                                            15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32)
        self.dropPatternDropDown.grid(row=1, column=self.clm(), sticky=NW)

        patternHelperButton = Button(self.top, text="Add Drop", command=self.addDrop)
        patternHelperButton.grid(row=1, column=self.clm(), sticky=NW)

        self.textPad = ScrolledText(self.top,width=40, height=10,font=label_font)
        self.textPad.grid(row=2, column=0, columnspan=columnTotal, sticky=NW)
        self.textPad.insert(END, self.parent.trackText.get())
        #for i in range(self.clmct+1):
            #self.top.grid_columnconfigure(i, weight=1, uniform="foo")


        okbtn = Button(self.top, text="Ok",command=self.saveText)
        okbtn.grid(row=3, column=0)
        cancelbtn = Button(self.top, text="Cancel")
        cancelbtn.grid(row=3,  column=1)
        menu = Menu(self.top)
        self.top.config(menu=menu)
        filemenu = Menu(menu)
        menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="New", command=self.dummy)
        filemenu.add_command(label="Open...", command=self.open_command)
        filemenu.add_command(label="Save", command=self.save_command)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.exit_command)
        helpmenu = Menu(menu)
        menu.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About...", command=self.about_command)

        #self.top.pack(side="top", fill="both", expand=True)