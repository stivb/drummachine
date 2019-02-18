import Tkinter
from Tkinter import *
from ScrolledText import *
import tkFileDialog
import tkMessageBox
import tkFont



# create a menu & define functions for each menu item

class Editor:

    def __init__(self,parentself,txt):
        self.txt = txt
        self.parent = parentself

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


    def init_ui(self):
        self.top = Toplevel(self.parent.root)
        self.top.geometry('800x600')
        label_font = tkFont.Font(family='Courer', size=25)
        textPad = ScrolledText(self.top, width=120, height=15,font=label_font)
        textPad.grid(row=0, column=0, columnspan=4, sticky=N)
        okbtn = Button(self.top, text="Ok")
        okbtn.grid(row=1, column=0)
        cancelbtn = Button(self.top, text="Cancel")
        cancelbtn.grid(row=2,  column=0)
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

