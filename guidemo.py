from Tkinter import *


class Buttons(Frame):
    def __init__(self, master):
        self.master = master
        self.button1 = Button(self.master, text='B1', width=25, command=self.addtxt1)
        self.button2 = Button(self.master, text='B2', width=25, command=self.addtxt2)
        self.button1.pack()
        self.button2.pack()

class Labels(Frame):
    def __init__(self, master):
        self.master = master
        var1 = StringVar()
        var2 = StringVar()
        self.label1 = Label(self.master, textvariable=var1, relief=RAISED)
        self.label2= Label(self.master, textvariable=var2, relief=RAISED)
        self.label1.pack()
        self.label2.pack()


class Demo1:
    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)
        self.buttonz = Buttons(self.frame)
        self.labelz = 


class Demo2:
    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)
        self.quitButton = Button(self.frame, text = 'Quit', width = 25, command = self.close_windows)
        self.quitButton.pack()
        self.frame.pack()
    def close_windows(self):
        self.master.destroy()

def main():
    root = Tk()
    app = Demo1(root)
    root.mainloop()

if __name__ == '__main__':
    main()