from Tkinter import *


def label_released():
    print "label_released"

def play_back():
    print "play_back"

def key_pressed():
    print "key_pressed"

def key_released():
    print "key_released"

def record_on_off():
    print "record_on_off"

def button_pressed():
    print "button_pressed"

def showdlg():
    print "show dialog"
    d = MyDialog(root)
    root.wait_window(d.top)

class MyDialog:

    def __init__(self, parent):

        top = self.top = Toplevel(parent)

        app = Piano(top)
        app.mainloop()

    #     Label(top, text="Value").pack()
    #
    #     self.e = Entry(top)
    #     self.e.pack(padx=5)
    #
    #     b = Button(top, text="OK", command=self.ok)
    #     b.pack(pady=5)
    #
    # def ok(self):
    #
    #     print "value is", self.e.get()
    #
    #     self.top.destroy()


class Piano(Frame):

    ##########################################################
    # Description: __init__ is a method that creates         #
    # the window, colors it and calls init_user_interface.   #
    #                                                        #
    # Accepts: self, which contains the window; parent,      #
    # which is a reference to the window.                    #
    ##########################################################
    def __init__(self, parent):

        # This is the initialization of the window along with the
        # coloring of the background.
        Frame.__init__(self, parent, background='SkyBlue3')

        # So that the parent reference does not go out of scope.
        self.parent = parent

        # A call to the init_user_interface method.
        self.init_user_interface()

    ##########################################################
    # Description: init_user_interface is a method that      #
    # populates the window passed in all of the Labels,      #
    # sizes the window, titles it, centers it on the screen  #
    # and binds various methods to it.                       #
    #                                                        #
    # Accepts: self, which contains the window.              #
    ##########################################################
    def init_user_interface(self):

        # The 2-dimensional array keys holds the locations, names and after the
        # for loops are executed below, the Labels that are needed
        # to create each key, both white and black.
        keys = [
            [0, 'C1'],
            [35, 'C#1'],
            [50, 'D1'],
            [85, 'D#1'],
            [100, 'E1'],
            [150, 'F1'],
            [185, 'F#1'],
            [200, 'G1'],
            [235, 'G#1'],
            [250, 'A1'],
            [285, 'A#1'],
            [300, 'B1'],
            [350, 'C2'],
            [385, 'C#2'],
            [400, 'D2'],
            [435, 'D#2'],
            [450, 'E2'],
            [500, 'F2'],
            [535, 'F#2'],
            [550, 'G2'],
            [585, 'G#2'],
            [600, 'A2'],
            [635, 'A#2'],
            [650, 'B2']
        ]

        # This for loop populates the window with the white key Labels
        # and appends a Label to each slot in keys.
        for key in keys:
            if len(key[1]) == 2:
                img = 'pictures/white_key.gif'
                key.append(self.create_key(img, key))

        # This for loop populates the window with the black key Labels
        # and appends a Label to each slot in keys.
        for key in keys:
            if len(key[1]) > 2:
                img = 'pictures/black_key.gif'
                key.append(self.create_key(img, key))

        # This group of lines creates the record Label.
        img = PhotoImage(file='pictures/red_button.gif')
        record_button = Label(self, image=img, bd=0)
        record_button.image = img
        record_button.place(x=700, y=0)
        record_button.name = 'red_button'
        record_button.bind('<Button-1>', record_on_off)

        # This group of lines creates the play Label.
        img = PhotoImage(file='pictures/green_button.gif')
        play_button = Label(self, image=img, bd=0)
        play_button.image = img
        play_button.place(x=700, y=50)
        play_button.name = 'green_button'
        play_button.bind('<Button-1>', play_back)
        play_button.bind('<ButtonRelease-1>', label_released)

        # This titles the window.
        self.parent.title('The Piano')

        # This group of lines centers the window on the screen
        # and specifies the size of the window.
        w = 750
        h = 200
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        x = (sw - w) / 2
        y = (sh - h) / 2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

        # This group of lines saves a reference to keys so that
        # it does not go out of scope and binds the presses and
        # releases of keys to their respective methods
        self.parent.keys = keys
        self.parent.bind('<KeyPress>', key_pressed)
        self.parent.bind('<KeyRelease>', key_released)

        # These 2 lines bind the '1' and '2' keys on the keyboard
        # to the playback method, which then hooks them up to their
        # respective files. This is mostly for demonstration and
        # experimentation purposes.
        self.parent.bind('1', play_back)
        self.parent.bind('2', play_back)

        # This line packs all elements bound to the window.
        self.pack(fill=BOTH, expand=1)

    ##########################################################
    # Description: create_key is a method that creates and   #
    # returns a Label with an image, a location, a name and  #
    # multiple bindings.                                     #
    #                                                        #
    # Accepts: self, the Piano class; img, the image that    #
    # the Label will be displayed as; key, the element of    #
    # the 2-dimensional array passed in.                     #
    ##########################################################
    def create_key(self, img, key):
        key_image = PhotoImage(file=img)
        label = Label(self, image=key_image, bd=0)
        label.image = key_image
        label.place(x=key[0], y=0)
        label.name = key[1]
        label.bind('<Button-1>', button_pressed)
        label.bind('<ButtonRelease-1>', label_released)
        return label



root = Tk()
Button(root, text="Hello!", command=showdlg).pack()
root.update()
root.mainloop(0)

