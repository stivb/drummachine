from Tkinter import *

class MyDialog:

    def __init__(self, parent):

        top = self.top = Toplevel(parent)

        Label(top, text="Value").pack()

        self.e = Entry(top,textvariable=txt)
        self.e.pack(padx=5)

        b = Button(top, text="OK", command=self.ok)
        b.pack(pady=5)

    def ok(self):

        print "value is", self.e.get()
        print "value is", txt.get()

        self.top.destroy()

    def showDlg(self):
        q = MyDialog(root)


def showDlg():
    d = MyDialog(root)

root = Tk()
txt = StringVar()
txt.set("1")

Button(root, text="Hello!", command=showDlg).pack()
root.update()



root.mainloop()

