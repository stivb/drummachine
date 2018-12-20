# -*- coding: utf-8 -*-

try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.resizable(width=False, height=False)

        # list variables
        self.list_var1 = tk.StringVar()
        self.list_var2 = tk.StringVar()

        # main frame
        self.main_frame = tk.Frame(self)

        self.listbox1 = tk.Listbox(self.main_frame, listvariable=self.list_var1, selectmode='multiple')
        self.listbox2 = tk.Listbox(self.main_frame, listvariable=self.list_var2, selectmode='multiple')

        # little button frame
        self.lr_button_frame = tk.Frame(self.main_frame)
        self.ud_button_frame = tk.Frame(self.main_frame)

        self.all_to_right_button = tk.Button(self.lr_button_frame, text='>', command=self.move_to_right)
        self.all_to_left_button = tk.Button(self.lr_button_frame, text='<', command=self.move_to_left)

        self.all_up_button = tk.Button(self.ud_button_frame, text='↑', command=self.move_up)
        self.all_down_button = tk.Button(self.ud_button_frame, text='↓', command=self.move_down)


        # packing
        self.all_to_right_button.pack()
        self.all_to_left_button.pack()

        self.all_up_button.pack()
        self.all_down_button.pack()

        self.listbox1.pack(side='left', anchor='w')
        self.lr_button_frame.pack(side='left')
        self.listbox2.pack(side='left', anchor='w')
        self.ud_button_frame.pack(side='right')
        self.main_frame.pack()

        # insert default values
        self.init_default_values()

    def init_default_values(self):

        a = [1, 2, 3, 4, 5]
        b = [6, 7, 8]
        self.listbox1.insert("end", *a)
        self.listbox2.insert("end", *b)

    def move_up(self):
        l = self.listbox2
        poslist = l.curselection()
        # exit if the list is empty
        if not poslist:
            return

        for pos in poslist:
            # skip if item is at the top
            if pos == 0:
                continue
            text = l.get(pos)
            l.delete(pos)
            l.insert(pos - 1, text)

    def move_down(self):
        l = self.listbox2
        max = self.listbox2.size()-1
        poslist = l.curselection()

        # exit if the list is empty
        if not poslist:
            return

        poslist = reversed(poslist)

        for pos in poslist:
            # skip if item is at the top
            if pos == max:
                continue
            text = l.get(pos)
            l.delete(pos)
            l.insert(pos +1, text)


    def moveItems(self, LB1, LB2):
        if LB1.curselection() == ():
            return


        selection = LB1.curselection()

        l1 = []
        l2 = []
        lsel = []

        ll1 = []
        ll2 = []


        for i, listbox_entry in enumerate(LB1.get(0, tk.END)):
            l1.append(listbox_entry)

        for i, listbox_entry in enumerate(LB2.get(0, tk.END)):
            l2.append(listbox_entry)

        for i in range(len(selection)):
            lsel.append(LB1.get(selection[i]))


        ll1 = [x for x in l1 if x not in lsel]
        l2.extend(lsel)

        LB1.delete(0, 'end')
        LB2.delete(0, 'end')

        LB1.insert("end", *ll1)
        LB2.insert("end", *l2)


    def move_to_right(self):
        self.moveItems(self.listbox1,self.listbox2)

    def move_to_left(self):
        self.moveItems(self.listbox2, self.listbox1)



app = App()
app.mainloop()