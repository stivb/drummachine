'''
May 2017
@author: Burkhard
'''

from Tkinter import *
import ttk



class OOP():
    def __init__(self):
        self.win = Tk()
        self.win.title("Python GUI")
        self.createWidgets()

    def createWidgets(self):

        #creates "notebook"
        note = ttk.Notebook(self.win)

        for i in range(0, 8):
            mystr = str(i*32) + '-' + str((i*32)+32)

            #creates a frame from the notebook
            thistab = ttk.Frame(note)
            #adds teh frame to the notebook
            note.add(thistab, text=mystr)
            # packs it
            note.pack(expand=1, fill="both")
            # creates a "labelframe" inside the frame inside the notebook
            self.monty = ttk.LabelFrame(thistab, text=mystr + "x")
            # sets up a grid for it
            self.monty.grid(column=0, row=0, padx=8, pady=4)
            for j in range(i * 32, (i * 32) + 32):
                btn = Button(self.monty, text=str(j + 1), width=3)
                btn.grid(column=j, row=1)



#         for idx in range(len(buttonTypes)):
#             rel = factory.createButton(idx).getButtonConfig()[0]
#             fg  = factory.createButton(idx).getButtonConfig()[1]
#
#             action = tk.Button(self.monty, text="Button "+str(idx+1), relief=rel, foreground=fg)
#             action.grid(column=idx, row=1)

# ==========================
oop = OOP()
oop.win.mainloop()