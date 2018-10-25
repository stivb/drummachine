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
import math
import os
import time

#modules for playing sounds
import time
import wave

import threading
import pickle

import ttk

import pygame
import pygame.midi
import piano


#constants
MAX_DRUM_NUM = 5




def play_back():
    print "play_back"



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
        self.bpm=120
        pygame.mixer.pre_init(44100, -16, 2, 1024)
        pygame.mixer.init()
        pygame.init()
        pygame.midi.init()
        self.input_id = pygame.midi.get_default_input_id()
        self.port = pygame.midi.get_default_output_id()
        #self.port = 8
        self.midi_out = pygame.midi.Output(self.port, 0)
        self._print_device_info()
        print "the port is", self.port

        self.currNote=-1
        self.noteNowOn=-1
        self.bassNowOn=-1
        self.dict = {}
        self.mididict = {}
        self.notesOn = []
        self.keyNumz ={'C1':24,'C#1':25,'D1':26,'D#1':27,'E1':28,'F1':29,'F#1':30,'G1':31,'G#1':32,'A1':33,'A#1':34,'B1':35,'C2':36,'C#2':37,'D2':38,'D#2':39,'E2':40,'F2':41,'F#2':42,'G2':43,'G#2':44,'A2':45,'A#2':46,'B2':47,'C3':48,'C#3':49,'D3':50,'D#3':51}
        #self.addFileToDrumset("C:/Users/Stiv/OneDrive - University of Hertfordshire/2017-18/2017-18/b/7COM1071/drum_machine/loops/bassdrum1.wav",0)
        #self.addFileToDrumset("C:/Users/Stiv/OneDrive - University of Hertfordshire/2017-18/2017-18/b/7COM1071/drum_machine/loops/snare.high.wav",1)
        self.deviceDict = self._midi_dev_dict()
        self.transpose = 0

        self.btnW = 6
        self.btnH = 4
        self.prevTime = time.clock()

    def about(self):
        tkMessageBox.showinfo("About","Tkinter GUI Application\n Development Hotshot")

    def key_pressed(self, event):
        c = repr(event.char)
        print "pressed ",c


    def key_released(self, event):

        print "released ", event.char

        if event.char == "a":
            print "yes"
            self.hitDrum("_0")
        if event.char == 's':
            self.hitDrum("_1")
        if event.char == 'd':
            self.hitDrum("_2")
        if event.char == 'f':
            self.hitDrum("_3")


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
                    self.buttonpickleformat[i][j] = self.buttonrowz[i][j].cget('text')
                else:
                    self.buttonpickleformat[i][j] = ' '
        self.pattern_list[prevpval] = {'df': self.widget_drum_file_name, 'bl': self.buttonpickleformat, 'bpu':bpu, 'units':units}
        self.reconstruct_pattern(pattern_num, bpu, units)



    def printTimeElapsed(self,msg):
        currTime = time.clock()
        print msg, currTime-self.prevTime
        self.prevTime=currTime


    def reconstruct_pattern(self,pattern_num, bpu, units):
        self.prevTime = time.clock()
        # your code here
        self.printTimeElapsed("START RECONSTRUCT PATTERN")

        # self.widget_drum_file_name = [0]*MAX_DRUM_NUM
        # try:
        #     self.df = self.pattern_list[pattern_num]['df']
        #     for i in range(len(self.df)):
        #             file_name = self.df[i]
        #             if file_name == 0:
        #                 self.widget_drum_name[i].delete(0, END)
        #                 continue
        #             self.widget_drum_file_name.insert(i, file_name)
        #             drum_name = os.path.basename(file_name)
        #             self.widget_drum_name[i].delete(0, END)
        #             self.widget_drum_name[i].insert(0, drum_name)
        # except:
        #         for i in range(MAX_DRUM_NUM):
        #             try: self.df
        #             except:self.widget_drum_name[i].delete(0, END)

        # self.printTimeElapsed("AFTER FIRST LOOP")
        # try:
        #     bpu = self.pattern_list[pattern_num]['bpu']
        #     units = self.pattern_list[pattern_num]['units']
        # except:
        #     return
        #
        # self.printTimeElapsed("AFTER TRY CATCH")
        # self.bpu_widget.delete(0, END)
        # self.bpu_widget.insert(0, bpu)
        # self.units_widget.delete(0, END)
        # self.units_widget.insert(0, units)
        # #self.createTimeLine()
        # c = bpu * units
        #self.createTimeLine()
        c = bpu * units
        self.printTimeElapsed("BEFORE RINSE TIMELINE")
        self.rinseTimeline(c,bpu)
        self.printTimeElapsed("AFTER CREATE TIMELINE")

        try:
            for i in range(MAX_DRUM_NUM):
                for j in range(c):
                    #if self.pattern_list[pattern_num]['bl'][i][j] == '*':
                    toPlay = self.pattern_list[pattern_num]['bl'][i][j]
                    if len(toPlay)>0 and toPlay!=" ":
                        self.buttonrowz[i][j].config(bg='green')
                        self.buttonrowz[i][j].config(text=toPlay)
        except:return
        self.printTimeElapsed("AFTER LAST LOOP")




    def play_in_thread(self):
        #print "About to play ",self.percPort, self.bassPort
        self.thread = threading.Thread(None,self.play, None, (), {})
        self.thread.start()

    def play(self):
                self.numMeasures = len(self.buttonrowz[0])
                self.thetime = time.time()
                self.keep_playing = True
                while self.keep_playing:
                      #self.button is an an array of button rows

                      for i in range(self.numMeasures):
                             self.colbtnz[i].config(bg='green')
                             if i>0:
                                 self.colbtnz[i-1].config(bg='white')
                             else:
                                 self.colbtnz[self.numMeasures-1].config(bg='white')

                             for thisrow in self.buttonrowz:
                                currentButton = thisrow[i]
                                currentRowNumber = self.buttonrowz.index(thisrow)
                                try:

                                    # if currentRowNumber==4:
                                    #     btnTxt = currentButton['text']
                                    #     if btnTxt!="":
                                    #         self.dict[btnTxt].play()
                                    #     print btnTxt

                                    if currentButton.cget('bg') == 'green':
                                        if currentRowNumber!=4:
                                            self.play_drum(self.row_to_drum_num(currentRowNumber))
                                        else:
                                            note_to_play = currentButton['text']
                                            if note_to_play != "":
                                                #print "looking to play", self.keyNumz[note_to_play]
                                                self.play_bass(self.keyNumz[note_to_play])



                                        #print "drum file name is: ", self.widget_drum_file_name[currentRowNumber]
                                        #print i, sound_filename, self.buttonrowz.index(item)
                                        #this line tests for no associated sound with the green ness


                                        #this part used to work!  check!
                                        #if not self.widget_drum_file_name[currentRowNumber]:continue
                                        #sound_filename = self.widget_drum_file_name[currentRowNumber]
                                        #self.dict[sound_filename].play()
                                except Exception as e:
                                    print "exception at ",i,str(e)
                                    continue
                             bpm_based_delay = (60.0/self.bpm)/4.0
                             #print bpm_based_delay
                             time.sleep(bpm_based_delay)
                             self.end_notes()
                             self.currNote = i
                             self.thetime = time.time()
                             if self.loop == False: self.keep_playing = False




    def row_to_drum_num(self,rownum):
        if rownum==0: return 36
        if rownum==1: return 38
        if rownum==2: return 40
        if rownum==3: return 42

    def play_drum(self,num):
        self.midi_out.set_instrument(50, channel=9)
        self.midi_out.note_on(num, 127,9)
        self.notesOn.append((num,9))

    def play_bass(self,num):
        num = num + self.transpose
        self.midi_out.set_instrument(65, channel=0)
        self.midi_out.note_on(num, 127,0)
        self.notesOn.append((num,0))

    def end_notes(self):
        for note in self.notesOn:
            #print "Note off",note[0],note[1]
            self.midi_out.note_off(note[0],None,note[1])
        self.notesOn=[]

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

        print self.dict


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
                self.change_beat(i,j,bpu)
            return callback


    def change_beat(self,i,j,bpu):
        btn = self.buttonrowz[i][j]
        color = 'grey55' if (j / bpu) % 2 else 'khaki'
        txt = ' '
        new_color = 'green' if btn.cget('bg') != 'green' else color
        new_text = '*' if (btn.cget('text') == '' or btn.cget('text') == ' ') else txt
        btn.config(bg=new_color)
        btn.config(text=new_text)

    def rinseTimeline(self, numCols, bpu):
        for i in range(MAX_DRUM_NUM):
            for j in range(numCols):
                color = 'grey55' if (j / bpu) % 2 else 'khaki'
                self.buttonrowz[i][j].config(text=' ',bg=color)
                #self.buttonrowz[i][j].config(bg=color)



    def bass_clicked(self, i, j, bpu):
            def callback():
                btn = self.buttonrowz[i][j]
                color = 'lightpink'
                if btn.cget('bg') != 'green':
                    piano.Piano(self,btn)
                    new_color='green'
                    self.addToDrumWidget("piano",4)
                else:
                    new_color=color
                    btn.config(text="")
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

        #playbar_frame.bind("<Key>", self.quay)


    def quay(self,event):
        print "pressed"

    def percValue(self,value):
        portId = self.deviceDict[value]
        print "The port is ", portId
        self.percPort = portId
        self.midi_out = pygame.midi.Output(self.percPort, 0)
        self.settingsPopup.destroy()



##        photo = PhotoImage(file='images/sig.gif')
##        label = Label(playbar_frame, image=photo)
##        label.image = photo
##        label.grid(row=ln, column=35,padx=1, sticky=E)


    def changeBpm(self):
        self.bpm = float(self.bpu_widget.get())
        print "bpm here is ", self.bpm

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



    def createTimeLine(self):
        bpu = self.bpu.get()
        units = self.units.get()
        c = bpu * units
        right_frame = Frame(self.root)
        right_frame.grid(row=10, column=0,sticky=W+E+N+S, padx=15, pady=2)

        self.buttonrowz = [[0 for x in range(c)] for x in range(MAX_DRUM_NUM)]
        self.colbtnz = [0 for x in range(c)]
        self.stopBtnz = [0 for x in range(c+1)] #needs extra one because going up to 32
        self.drumpads = [None]*MAX_DRUM_NUM
        self.clearpads = [None]*MAX_DRUM_NUM




        for q in range(c+1):
            btnName ="btnEnd"+ str(q)
            self.stopBtnz[q] = Button(right_frame, name=btnName, bg='white', text=str(q), width=self.btnW, height=self.btnH,command=self.stop_clicked(q))
            self.stopBtnz[q].grid(row=0, column=q)

        right_frame.grid_rowconfigure(1, minsize=20)

        for q in range(c):
            btnName ="col"+ str(q)
            numToShow = str(q % 12)
            self.colbtnz[q] = Button(right_frame, name=btnName, bg='white', text=numToShow, width=self.btnW, height=self.btnH, command=self.col_clicked(q))
            self.colbtnz[q].grid(row=2, column=q)



        right_frame.grid_rowconfigure(3,minsize=20)
        row_base = 4

        for i in range(MAX_DRUM_NUM):
            for j in range(c):
                self.active = False
                color = 'grey55' if (j/bpu)%2 else 'khaki'
                basscolor =  'lightpink'
                btnName = "btn" + str(i) + ":" + str(j)
                if i<MAX_DRUM_NUM-1:

                    self.buttonrowz[i][j] = Button(right_frame, name=btnName, bg=color, width=self.btnW, height=self.btnH, command=self.button_clicked(i, j,bpu))
                    #self.buttonrowz[i][j] = Button(right_frame, bg=color, width=1)
                    self.buttonrowz[i][j].bind('<Double-1>', self.percDblClicked)
                else:
                    self.buttonrowz[i][j] = Button(right_frame,  bg=basscolor, width=self.btnW, height=self.btnH, command=self.bass_clicked(i, j, bpu))

                self.buttonrowz[i][j].grid(row=i+row_base, column=j)
                #print "now at",j

            drumPadName= "d_" + str(i)
            self.drumpads[i] = Button(right_frame, name=drumPadName, bg=color, width=self.btnW, height=self.btnH, command=self.d_clicked(drumPadName))
            right_frame.grid_columnconfigure(j+1, minsize=10)
            self.drumpads[i].grid(row=i+row_base, column=j+2)

            #delPadName = "x" + str(i)
            #self.clearpads[i] = Button(right_frame, name=delPadName, bg=color, width=2, command=self.del_clicked(delPadName))
            #self.clearpads[i].grid(row=i, column=j + 4)

    def col_clicked(self,num):
        def callback():
            self.transpose = num
            print "self transpose is now ",self.transpose
        return callback

    def stop_clicked(self,num):
        def callback():
            self.numMeasures = num
            print "self numMeasures is now ",self.numMeasures
        return callback

    def d_clicked(self,dname):
        def callback():
            self.hitDrum(dname)
        return callback


    def hitDrum(self,dname):
        print dname
        if self.currNote < 0:
            return

        print "dclicked"
        print dname
        delay = (60.0 / self.bpm) / 4.0
        timesincenotechange = time.time() - self.thetime

        rowclicked = int(dname.split("_")[1])
        print rowclicked, self.currNote
        rowclicked = int(dname.split("_")[1])

        notepos = self.currNote
        if (timesincenotechange / delay > 0.5):
            self.buttonrowz[rowclicked][notepos].config(bg='green')
            self.buttonrowz[rowclicked][notepos].config(text='*')
        else:
            notepos = notepos - 1
            if notepos < 0: notepos = 31
            self.buttonrowz[rowclicked][notepos].config(bg='green')
            self.buttonrowz[rowclicked][notepos].config(text='*')



    def popupSettings(self):

        popup = Toplevel(self.root)
        self.settingsPopup = popup
        popup.geometry("302x115+900+237")
        percDevice = StringVar()

        # Dictionary with options

        percDevice.set('')  # set the default option

        # popupMenu = OptionMenu(playbar_frame, tkvar, *choices)
        percDeviceMenu = OptionMenu(popup, percDevice, *sorted(self.deviceDict.keys()), command=self.percValue)
        Label(popup, text="Midi Device").grid(row=0, column=0)
        percDeviceMenu.grid(row=0, column=2)

        for i in range(1,5):
            Label(popup, text="Drum" + str(i)).grid(row=i, column=0)


        popup.title("Major Settings")
        popup.configure(background="#d9d9d9")
        popup.wm_title("!")
        popup.mainloop()


    def del_clicked(self,xname):
        print xname

    def percDblClicked(self,event):
        a = str(event.widget).split(".")[-1]
        rw= a[3:].split(":")[0]
        cl = a[3:].split(":")[1]
        print rw
        print cl
        self.popupmsg(str(rw) + ":" + str(cl))

    def popupmsg(self, msg):

        popup = Toplevel(self.root)
        popup.geometry("302x115+645+237")
        popup.title("Add Beats")
        popup.configure(background="#d9d9d9")
        popup.wm_title("!")
        self.btn = [None]*5
        btnXpos = 0.17
        for i in range(5):
            btnName = "beats"+str(i)
            self.btn[i] = Button(popup,name=btnName,command = lambda name=str(int(math.pow(2,i+1))): self.add_beats(name,msg) and popup.destroy())
            self.btn[i].place(relx=btnXpos, rely=0.43, height=25, width=37)
            self.btn[i].configure(pady="0")
            self.btn[i].configure(text=str(int(math.pow(2,i+1))))
            btnXpos = btnXpos+ 0.13

        label = ttk.Label(popup, text=msg)
        label.pack(side="top", fill="x", pady=10)
        B1 = ttk.Button(popup, text="Cancel", command=popup.destroy)
        B1.place(relx=0.40,rely=0.70, height=25, width=50)
        popup.mainloop()

    def add_beats(self,num,msg):
        row = int(msg.split(':')[0])
        col = int(msg.split(':')[1])
        r = row
        c = col
        while col<32:
            #self.buttonrowz[row][col].config(bg='green')
            self.change_beat(row,col,self.bpu.get())
            col=col+int(num)
        self.change_beat(r, c, self.bpu.get())
        return True



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
        self.units.set(8)
        self.units_widget = Spinbox(topbar_frame, from_=1, to=8, width=5, textvariable=self.units, command=self.createTimeLine)
        self.units_widget.grid(row=0, column=5)

        Label(topbar_frame, text='BPUs:').grid(row=0, column=6)
        self.bpu = IntVar()
        self.bpu.set(4)
        self.bpu_widget = Spinbox(topbar_frame, from_=1, to=10, width=5, textvariable=self.bpu, command= self.createTimeLine)
        self.bpu_widget.grid(row=0, column=7)

        self.createTimeLine()

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
        self.aboutmenu.add_command(label="Settings", command=self.popupSettings)
        self.menubar.add_cascade(label="About", menu=self.aboutmenu)

        self.root.config(menu=self.menubar)


    def app(self):
        self.root = Tk()
        self.root.title('Drum Beast')
        self.top_menu()
        self.create_top_bar()
        #self.create_left_pad()
        self.create_play_bar()
        self.root.protocol('WM_DELETE_WINDOW', self.exit_app)
        if os.path.isfile('images/beast.ico'): self.root.wm_iconbitmap('images/beast.ico')
        self.root.bind('<KeyPress>', self.key_pressed)
        self.root.bind('<KeyRelease>', self.key_released)
        self.root.mainloop()
        self.popupmsg("hello")


    def key(event):
        print "pressed", repr(event.char)

    def _print_device_info(self):
        for i in range( pygame.midi.get_count() ):
            r = pygame.midi.get_device_info(i)
            (interf, name, input, output, opened) = r

            in_out = ""
            if input:
                in_out = "(input)"
            if output:
                in_out = "(output)"

            print ("%2i: interface :%s:, name :%s:, opened :%s:  %s" %
                   (i, interf, name, opened, in_out))

    def _midi_dev_dict(self):
        mydict = {}
        for i in range( pygame.midi.get_count() ):
            r = pygame.midi.get_device_info(i)
            (interf, name, input, output, opened) = r

            in_out = ""
            if input:
                in_out = "(input)"
            if output:
                in_out = "(output)"

            s ="{}: interface :{}:, name :{}:, opened :{}:  {}".format(i, interf, name, opened, in_out)
            mydict[s] = i
        return mydict





 
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


