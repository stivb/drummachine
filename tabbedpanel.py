'''
May 2017
@author: Burkhard
'''

from Tkinter import *
import ttk
from ScrolledText import *


class ButtonFactory():
    def createButton(self, type_):
        return buttonTypes[type_]()


class ButtonBase():
    relief = 'flat'
    foreground = 'white'

    def getButtonConfig(self):
        return self.relief, self.foreground


class ButtonRidge(ButtonBase):
    relief = 'ridge'
    foreground = 'red'


class ButtonSunken(ButtonBase):
    relief = 'sunken'
    foreground = 'blue'


class ButtonGroove(ButtonBase):
    relief = 'groove'
    foreground = 'green'


buttonTypes = [ButtonRidge, ButtonSunken, ButtonGroove]


class OOP():
    def __init__(self):
        self.win = Tk()
        self.win.title("Python GUI")
        self.createWidgets()

    def createWidgets(self):

        tabControls = []
        note = ttk.Notebook(self.win)

        for i in range(0, 8):
            mystr = str(i*32) + '-' + str((i*32)+32)

            thistab = ttk.Frame(note)
            tabControls.append(thistab)
            note.add(thistab, text=mystr)
            note.pack(expand=1, fill="both")
            self.monty = ttk.LabelFrame(thistab, text=mystr + "x")
            self.monty.grid(column=0, row=0, padx=8, pady=4)
            for j in range(i*32, (i*32)+32):
                btn = Button(self.monty, text=str(j+1),width=3)
                btn.grid(column=j, row=1)

    def createButtons(self):
        factory = ButtonFactory()

        # Button 1
        rel = factory.createButton(0).getButtonConfig()[0]
        fg = factory.createButton(0).getButtonConfig()[1]
        action = Button(self.monty, text="Button " + str(0 + 1), relief=rel, foreground=fg)
        action.grid(column=0, row=1)

        # Button 2
        rel = factory.createButton(1).getButtonConfig()[0]
        fg = factory.createButton(1).getButtonConfig()[1]
        action = Button(self.monty, text="Button " + str(1 + 1), relief=rel, foreground=fg)
        action.grid(column=1, row=1)

        # Button 3
        rel = factory.createButton(2).getButtonConfig()[0]
        fg = factory.createButton(2).getButtonConfig()[1]
        action = Button(self.monty, text="Button " + str(2 + 1), relief=rel, foreground=fg)
        action.grid(column=2, row=1)

    #         # using a loop to do the above


#         for idx in range(len(buttonTypes)):
#             rel = factory.createButton(idx).getButtonConfig()[0]
#             fg  = factory.createButton(idx).getButtonConfig()[1]
#
#             action = tk.Button(self.monty, text="Button "+str(idx+1), relief=rel, foreground=fg)
#             action.grid(column=idx, row=1)

# ==========================
oop = OOP()
oop.win.mainloop()