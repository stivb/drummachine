from Tkinter import *
import ttk
root = Tk()

style = ttk.Style()

style.layout('TNotebook.Tab', []) # turn off tabs

note = ttk.Notebook(root)

f1 = ttk.Frame(note)
txt = Text(f1, width=40, height=10)
txt.insert('end', 'Page 0 : a text widget')
txt.pack(expand=1, fill='both')
fl.add(tab1, text=mystr)
note.add(f1)

f2 = ttk.Frame(note)
lbl = Label(f2, text='Page 1 : a label')
lbl.pack(expand=1, fill='both')
note.add(f2)

note.pack(expand=1, fill='both', padx=5, pady=5)

def do_something():
    note.select(1)

root.after(1000, do_something)
root.mainloop()