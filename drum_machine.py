#!/usr/bin/env python
"""
Code illustration: 3.12
Finalizing our Drum Machine
adding comment
@Tkinter GUI Application Development Hotshot
"""


from Tkinter import *
import tkFileDialog
import tkMessageBox
import os

#modules for playing sounds
import time
import wave

import threading
import pickle

import ttk

import pygame

#constants
MAX_DRUM_NUM = 5




def play_back():
    print "play_back"

def key_pressed():
    print "key_pressed"

def key_released():
    print "key_released"

def record_on_off():
    print "record_on_off"





class DrumMachine():


    def __init__(self):
        self.widget_drum_name = []
        self.widget_drum_file_name = [0]*MAX_DRUM_NUM
        self.widget_drum_file_sound = [0]*MAX_DRUM_NUM
        self.current_drum_no = 0
        self.keep_playing = True
        self.loop = False
        self.pattern_list = [None]*10
        self.file1 = ""
        self.file2= ""
        self.file3=""
        self.file4=""
        self.file5=""
        self.bpm = 120.0/960.0
        pygame.mixer.pre_init(44100, -16, 2, 1024)
        pygame.mixer.init()
        pygame.init()
        self.dict = {}
        #self.addFileToDrumset("C:/Users/Stiv/OneDrive - University of Hertfordshire/2017-18/2017-18/b/7COM1071/drum_machine/loops/bassdrum1.wav",0)
        #self.addFileToDrumset("C:/Users/Stiv/OneDrive - University of Hertfordshire/2017-18/2017-18/b/7COM1071/drum_machine/loops/snare.high.wav",1)



    def about(self):
        tkMessageBox.showinfo("About","Tkinter GUI Application\n Development Hotshot")


    def exit_app(self):
        if tkMessageBox.askokcancel("Quit", "Do you really want to quit?"):
            self.root.destroy()


    def save_project(self):
        self.record_pattern()#make sure the last pattern is recorded before save
        file_name = tkFileDialog.asksaveasfilename(filetypes=[('Drum Beat File','*.bt')] , title="Save project as...")
        pickle.dump( self.pattern_list, open( file_name, "wb" ) )
        self.root.title(os.path.basename(file_name) + " - DrumBeast")



    def load_project(self):
        file_name = tkFileDialog.askopenfilename(filetypes=[('Drum Beat File','*.bt')], title='Load Project')
        if file_name == '':return
        self.root.title(os.path.basename(file_name) + " - DrumBeast")
        fh = open(file_name,"rb") # open the file in reading mode
        try:
         while True: # load from the file until EOF is reached
          self.pattern_list = pickle.load(fh)
        except EOFError:
          pass
        fh.close()
        try:
            self.reconstruct_pattern(0, self.pattern_list[0]['bpu'], self.pattern_list[0]['units'])# reconstruct the first pattern
        except:tkMessageBox.showerror("Error","An unexpected error occurred trying to reconstruct patterns")


    def record_pattern(self):
        pattern_num, bpu, units = self.patt.get(),self.bpu.get(), self.units.get()
        self.pat_name.config(state='normal')
        self.pat_name.delete(0, END)
        self.pat_name.insert(0, 'Pattern %s'%pattern_num)
        self.pat_name.config(state='readonly')
        prevpval = self.prevpatvalue
        self.prevpatvalue = pattern_num
        c = bpu*units
        self.buttonpickleformat = [[0] * c for x in range(MAX_DRUM_NUM)]
        for i in range(MAX_DRUM_NUM):
            for j in range(c):
                if self.buttonrowz[i][j].config('bg')[-1] == 'green':
                    self.buttonpickleformat[i][j] = 'active'
        self.pattern_list[prevpval] = {'df': self.widget_drum_file_name, 'bl': self.buttonpickleformat, 'bpu':bpu, 'units':units}
        self.reconstruct_pattern(pattern_num, bpu, units)




    def reconstruct_pattern(self,pattern_num, bpu, units):
        self.widget_drum_file_name = [0]*MAX_DRUM_NUM
        try:
            self.df = self.pattern_list[pattern_num]['df']
            for i in range(len(self.df)):
                    file_name = self.df[i]
                    if file_name == 0:
                        self.widget_drum_name[i].delete(0, END)
                        continue
                    self.widget_drum_file_name.insert(i, file_name)
                    drum_name = os.path.basename(file_name)
                    self.widget_drum_name[i].delete(0, END)
                    self.widget_drum_name[i].insert(0, drum_name)
        except:
                for i in range(MAX_DRUM_NUM):
                    try: self.df
                    except:self.widget_drum_name[i].delete(0, END)
        try:
            bpu = self.pattern_list[pattern_num]['bpu']
            units = self.pattern_list[pattern_num]['units']
        except:
            return
        self.bpu_widget.delete(0, END)
        self.bpu_widget.insert(0, bpu)
        self.units_widget.delete(0, END)
        self.units_widget.insert(0, units)
        self.create_right_pad()
        c = bpu * units
        self.create_right_pad()
        try:
            for i in range(MAX_DRUM_NUM):
                for j in range(c):
                    if self.pattern_list[pattern_num]['bl'][i][j] == 'active':
                        self.buttonrowz[i][j].config(bg='green')
        except:return




    def play_in_thread(self):
        self.thread = threading.Thread(None,self.play, None, (), {})
        self.thread.start()

    def play(self):
                self.keep_playing = True
                while self.keep_playing:
                      #self.button is an an array of button rows
                      buttoncolzlength = len(self.buttonrowz[0])
                      for i in range(buttoncolzlength):
                             for thisrow in self.buttonrowz:
                                currentButton = thisrow[i]
                                currentRowNumber = self.buttonrowz.index(thisrow)
                                try:

                                    if currentRowNumber==4:
                                        btnTxt = currentButton['text']
                                        if btnTxt!="":
                                            self.dict[btnTxt].play()
                                        print btnTxt

                                    if currentButton.cget('bg') == 'green':
                                        print "drum file name is: ", self.widget_drum_file_name[currentRowNumber]
                                        #print i, sound_filename, self.buttonrowz.index(item)
                                        #this line tests for no associated sound with the green ness
                                        if not self.widget_drum_file_name[currentRowNumber]:continue
                                        sound_filename = self.widget_drum_file_name[currentRowNumber]
                                        self.dict[sound_filename].play()
                                except Exception as e:
                                    print "exception at ",i,str(e)
                                    continue
                             print int(round(time.time() * 1000))
                             time.sleep(0.5/4)
                             if self.loop == False: self.keep_playing = False



  
 

  
    def stop_play(self):
        self.keep_playing = False
        return

    def loop_play(self, xval):
        self.loop = xval

    def addFileToDrumset(self, file_name, drum_no):

        try:
            del self.widget_drum_file_name[drum_no]
        except:
            pass
        self.widget_drum_file_name.insert(drum_no, file_name)
        # line added by me

        self.dict[file_name] = pygame.mixer.Sound(file_name)
        self.widget_drum_file_sound.insert(drum_no, pygame.mixer.Sound(file_name))
        # self.widget_drum_file_sound[drum_no].play()
        self.dict[file_name].play()
        # end me

        # self.dict[file_name] = soundThing(pygame.mixer(), file_name, drum_no)
        # self.dict[file_name].play()

        drum_name = os.path.basename(file_name)

        self.addToDrumWidget(file_name,drum_no)


    def addToDrumWidget(self,drum_name,drum_no):
        #basically this is clearing and filling  a text box
        self.widget_drum_name[drum_no].delete(0, END)
        self.widget_drum_name[drum_no].insert(0, drum_name)
        print "inserting this", self.widget_drum_name[drum_no]


    def drum_load(self, drum_no):
        def callback():
            self.current_drum_no = drum_no
            try:
                file_name = tkFileDialog.askopenfilename(defaultextension=".wav",filetypes=[("Wave Files","*.wav"),("OGG Files","*.ogg")])
                if not file_name: return
                print file_name,drum_no
                self.addFileToDrumset(file_name,drum_no)

            except:
                tkMessageBox.showerror('Invalid', "Error loading drum samples")
        return callback

    def bass_load(self, drum_no,note):
        def callback():
            pth = os.path.dirname(os.path.realpath(__file__))
            file_name = pth + "\\notes\\" + note + ".wav"
            self.current_drum_no = drum_no
            try:
                if not file_name: return
                print file_name,drum_no
                self.addFileToDrumset(file_name,drum_no)

            except:
                tkMessageBox.showerror('Invalid', "Error loading drum samples")
        return callback


    def button_clicked(self,i,j,bpu):
            def callback():
                btn = self.buttonrowz[i][j]
                color = 'grey55' if (j/bpu)%2 else 'khaki'
                new_color = 'green' if btn.cget('bg') != 'green' else color
                btn.config(bg=new_color)
            return callback


    def bass_clicked(self, i, j, bpu):
            def callback():
                btn = self.buttonrowz[i][j]
                color = 'lightpink'
                if btn.cget('bg') != 'green':
                    Piano(self,btn)
                    new_color='green'
                    self.addToDrumWidget("piano",4)
                else:
                    new_color=color
                print color,btn.cget('bg'),new_color
                btn.config(bg=new_color)
            return callback

    def create_play_bar(self):
        playbar_frame = Frame(self.root, height=15)
        ln = MAX_DRUM_NUM+10
        playbar_frame.grid(row=ln, columnspan=13,sticky=W+E,padx=15, pady=10)
        button = ttk.Button( playbar_frame, text ='Play', command= self.play_in_thread)
        button.grid(row= ln, column=1, padx=1)
        button = ttk.Button( playbar_frame, text ='Stop', command= self.stop_play)
        button.grid(row= ln, column=3,padx=1)
        loop = BooleanVar()
        loopbutton = ttk.Checkbutton(playbar_frame, text='Loop', variable=loop, command=lambda: self.loop_play(loop.get()))
        loopbutton.grid(row=ln, column=16,padx=1)

        Label(playbar_frame, text='BPM:').grid(row=ln, column=35, padx=30)
        self.bpmTxt = StringVar()
        self.bpmTxt.set(120)
        self.bpu_widget = Spinbox(playbar_frame, from_=80, to=160, width=5, textvariable=self.bpmTxt, command= self.changeBpm)
        self.bpu_widget.grid(row=ln, column=45)




##        photo = PhotoImage(file='images/sig.gif')
##        label = Label(playbar_frame, image=photo)
##        label.image = photo
##        label.grid(row=ln, column=35,padx=1, sticky=E)


    def changeBpm(self):
        self.bpm = float(self.bpu_widget.get())/960.0
        print self.bpm

    def create_left_pad(self):
        '''creating actual pattern editor pad'''
        left_frame = Frame(self.root)
        left_frame.grid(row=10, column=0, columnspan=6,sticky=W+E+N+S)
        tbicon = PhotoImage(file='images/openfile.gif')
        for i in range(0, MAX_DRUM_NUM):
            button = Button(left_frame, image=tbicon, command= self.drum_load(i))
            button.image = tbicon
            button.grid(row=i, column=0,  padx=5,pady=2)
            self.drum_entry = Entry(left_frame)
            self.drum_entry.grid(row=i, column=4, padx=7,pady=2)
            self.widget_drum_name.append(self.drum_entry)




    def create_right_pad(self):
        bpu = self.bpu.get()
        units = self.units.get()
        c = bpu * units
        right_frame = Frame(self.root)
        right_frame.grid(row=10, column=6,sticky=W+E+N+S, padx=15, pady=2)
        self.buttonrowz = [[0 for x in range(c)] for x in range(MAX_DRUM_NUM)]
        for i in range(MAX_DRUM_NUM):
            for j in range(c):
                self.active = False
                color = 'grey55' if (j/bpu)%2 else 'khaki'
                basscolor =  'lightpink'
                print i,MAX_DRUM_NUM
                if i<MAX_DRUM_NUM-1:
                    self.buttonrowz[i][j] = Button(right_frame, bg=color, width=1, command=self.button_clicked(i, j, bpu))
                else:
                    self.buttonrowz[i][j] = Button(right_frame, bg=basscolor, width=1, command=self.bass_clicked(i, j, bpu))
                self.buttonrowz[i][j].grid(row=i, column=j)


    def create_top_bar(self):
        '''creating top buttons'''
        topbar_frame = Frame(self.root)
        topbar_frame.config(height=25)
        topbar_frame.grid(row=0, columnspan=12, rowspan=10, padx=5, pady=5)

        Label(topbar_frame, text='Pattern Number:').grid(row=0, column=1)
        self.patt = IntVar()
        self.patt.set(0)
        self.prevpatvalue = 0 # to trace last click
        Spinbox(topbar_frame, from_=0, to=9, width=5, textvariable=self.patt, command=self.record_pattern).grid(row=0, column=2)
        self.pat_name = Entry(topbar_frame)
        self.pat_name.grid(row=0, column=3, padx=7,pady=2)
        self.pat_name.insert(0, 'Pattern %s'%self.patt.get())
        self.pat_name.config(state='readonly')


        Label(topbar_frame, text='Units:').grid(row=0, column=4)
        self.units = IntVar()
        self.units.set(4)
        self.units_widget = Spinbox(topbar_frame, from_=1, to=8, width=5, textvariable=self.units, command=self.create_right_pad)
        self.units_widget.grid(row=0, column=5)

        Label(topbar_frame, text='BPUs:').grid(row=0, column=6)
        self.bpu = IntVar()
        self.bpu.set(4)
        self.bpu_widget = Spinbox(topbar_frame, from_=1, to=10, width=5, textvariable=self.bpu, command= self.create_right_pad)
        self.bpu_widget.grid(row=0, column=7)

        self.create_right_pad()

    def top_menu(self):
        self.menubar = Menu(self.root)

        self.filemenu = Menu(self.menubar, tearoff=0 )
        self.filemenu.add_command(label="Load Project", command=self.load_project )
        self.filemenu.add_command(label="Save Project", command=self.save_project)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.exit_app)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.aboutmenu = Menu(self.menubar, tearoff=0 )
        self.aboutmenu.add_command(label="About", command=self.about)
        self.menubar.add_cascade(label="About", menu=self.aboutmenu)

        self.root.config(menu=self.menubar)


    def app(self):
        self.root = Tk()
        self.root.title('Drum Beast')
        self.top_menu()
        self.create_top_bar()
        self.create_left_pad()
        self.create_play_bar()
        self.root.protocol('WM_DELETE_WINDOW', self.exit_app)
        if os.path.isfile('images/beast.ico'): self.root.wm_iconbitmap('images/beast.ico')
        self.root.mainloop()





class Piano:


    ##########################################################
    # Description: __init__ is a method that creates         #
    # the window, colors it and calls init_user_interface.   #
    #                                                        #
    # Accepts: self, which contains the window; parent,      #
    # which is a reference to the window.                    #
    ##########################################################
    def __init__(self, parentself,srcBtn):

        # This is the initialization of the window along with the
        # coloring of the background.
        #Frame.__init__(self, parent, background='SkyBlue3')

        self.top = Toplevel(parentself.root)

        self.parentself = parentself

        # So that the parent reference does not go out of scope.
        self.parent = parentself.root

        self.btn = srcBtn
        self.dict = parentself.dict

        # A call to the init_user_interface method.
        self.init_user_interface()


        #print self.btn

    def label_released(self,other):
        print other.widget.name
        self.btn.config(text=other.widget.name)
        self.btn.config(bg='green')

    def button_pressed(self,other):
        note= other.widget.name
        self.btn.config(text=note)
        self.dict[note].play()
        self.btn.config(bg='green')
        self.parentself.bass_load(note,4)
        self.top.destroy()
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

        for key in keys:
            self.dict[key[1]] =  pygame.mixer.Sound('notes/' + key[1] + '.wav')

        # This group of lines creates the record Label.
        img = PhotoImage(file='pictures/red_button.gif')
        record_button = Label(self.top, image=img, bd=0)
        record_button.image = img
        record_button.place(x=700, y=0)
        record_button.name = 'red_button'
        record_button.bind('<Button-1>', record_on_off)

        # This group of lines creates the play Label.
        img = PhotoImage(file='pictures/green_button.gif')
        play_button = Label(self.top, image=img, bd=0)
        play_button.image = img
        play_button.place(x=700, y=50)
        play_button.name = 'green_button'
        play_button.bind('<Button-1>', play_back)
        #play_button.bind('<ButtonRelease-1>', label_released)

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
        self.top.geometry('%dx%d+%d+%d' % (w, h, x, y))

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
        #self.pack(fill=BOTH, expand=1)

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
        label = Label(self.top, image=key_image, bd=0)
        label.image = key_image
        label.place(x=key[0], y=0)
        label.name = key[1]
        label.bind('<Button-1>', self.button_pressed)
        label.bind('<ButtonRelease-1>', self.label_released)
        print key
        return label
 
class soundThing():
    def __init__(self,pgmixer,fn,ch):
        self.filename=fn
        self.channelNumber=ch
        self.pyGameMixer=pgmixer
        self.snd = pgmixer.Sound(fn)


    def play(self):
        self.pyGameMixer.Channel(self.channelNumber).play(self.snd)

# ======================================================================
if __name__ == '__main__':

    dm = DrumMachine()
    dm.app()


