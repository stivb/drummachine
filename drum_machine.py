#!/usr/bin/env python
"""
Code illustration: 3.12
Finalizing our Drum Machine
adding comment
@Tkinter GUI Application Development Hotshot
"""

from Tkinter import *
import SimpleDialog
import tkFileDialog
import listfiles
import tkMessageBox
import math
import os
import time
import datetime
import copy
import ConfigParser
import copy
import copybars
import get_preferred_xy

# modules for playing sounds
import time
import wave

import threading
import pickle

import ttk

import pygame
import pygame.midi
import piano
import song
import instrumentchannel
import editor
import newsongdlg
import MidiWriter

# constants
MAX_TRACK_NUM = 6


def play_back():
    print "play_back"


def record_on_off():
    print "record_on_off"

def after_startup():
    print "whatever"


class DrumMachine:

    def __init__(self, w, h):

        print "init"
        self.btnW = w
        self.btnH = h

        self.kbd = "awsdrftghujikol;[']#"
        self.kbdmappings = {'a':'A1','w':'A#1','s':'B1','d':'C2','r':'C#2','f':'D2','t':'D#2','g':'E2','h':'F2','u':'F#2','j':'G2','i':'G#2','k':'A2','o':'A#2','l':'B2',';':'C3','[':'C#3','\'':'D3',']':'D#3','#':'E3'}
        self.recordOnChange = True
        self.widget_drum_name = []
        self.widget_drum_file_name = [0] * MAX_TRACK_NUM
        self.widget_drum_file_sound = [0] * MAX_TRACK_NUM
        self.current_drum_no = 0
        self.keep_playing = True
        self.loop = False
        self.seq = False
        self.pattern_list = [None] * 256
        self.file1 = ""
        self.file2 = ""
        self.file3 = ""
        self.file4 = ""
        self.file5 = ""
        self.patternHasChanged = False

        self.bpm = 120
        print "before pygame mixer preinit"
        pygame.mixer.pre_init(44100, -16, 2, 1024)
        print "before pygame mixier init"
        time.sleep(1)
        pygame.mixer.init()
        print "before pygame init"
        time.sleep(1)
        pygame.init()
        time.sleep(1)
        print "before pygame midi init"
        pygame.midi.init()
        time.sleep(1)
        print "midi init"
        self.input_id = pygame.midi.get_default_input_id()
        self.port = pygame.midi.get_default_output_id()
        # self.port = 8
        self.midi_out = pygame.midi.Output(self.port, 0)
        self._print_device_info()
        print "the port is", self.port
        self.queuedPattern = 0
        self.clipboardTrack = []
        self.saveWhileLooping= False

        # self.patt.set(0)
        # self.root = Tk()
        # gself.patt =  IntVar()

        self.currNote = -1
        self.noteNowOn = -1
        self.bassNowOn = -1
        self.dict = {}
        self.mididict = {}
        self.notesOn = []
        self.keyNumz = {'C1': 24, 'C#1': 25, 'D1': 26, 'D#1': 27, 'E1': 28, 'F1': 29, 'F#1': 30, 'G1': 31, 'G#1': 32,
                        'A1': 33, 'A#1': 34, 'B1': 35, 'C2': 36, 'C#2': 37, 'D2': 38, 'D#2': 39, 'E2': 40, 'F2': 41,
                        'F#2': 42, 'G2': 43, 'G#2': 44, 'A2': 45, 'A#2': 46, 'B2': 47, 'C3': 48, 'C#3': 49, 'D3': 50,
                        'D#3': 51}

        self.notes = ['C1', 'C#1', 'D1', 'D#1', 'E1', 'F1', 'F#1', 'G1', 'G#1',  'A1', 'A#1', 'B1', 'C2', 'C#2', 'D2', 'D#2', 'E2', 'F2', 'F#2', 'G2', 'G#2', 'A2', 'A#2', 'B2', 'C3', 'C#3', 'D3','D#3']
        # self.addFileToDrumset("C:/Users/Stiv/OneDrive - University of Hertfordshire/2017-18/2017-18/b/7COM1071/drum_machine/loops/bassdrum1.wav",0)
        # self.addFileToDrumset("C:/Users/Stiv/OneDrive - University of Hertfordshire/2017-18/2017-18/b/7COM1071/drum_machine/loops/snare.high.wav",1)
        self.deviceDict = self._midi_dev_dict()
        self.transpose = 0
        self.hitList = {}


        self.prevTime = time.clock()
        self.channels = []
        self.channels.append(instrumentchannel.InstrumentChannel(self, 36 , 127, 9))
        self.channels.append(instrumentchannel.InstrumentChannel(self, 38, 127, 9))
        self.channels.append(instrumentchannel.InstrumentChannel(self, 40, 127, 9))
        self.channels.append(instrumentchannel.InstrumentChannel(self, 42, 127, 9))
        self.channels.append(instrumentchannel.InstrumentChannel(self, 32, 127, 0))
        self.channels.append(instrumentchannel.InstrumentChannel(self, 33, 127, 1))
        self.currentPattern = 0
        self.breaks=[]
        self.patternToCopy = -1

        self.ed = editor.Editor(self)
        self.trackText = None


    def app(self):
        print "Trying to start"
        self.root = Tk()
        self.root.title('Drum Beast')
        self.top_menu()
        self.create_top_bar()
        print "still trying"
        # self.create_left_pad()
        self.create_play_bar()
        self.root.protocol('WM_DELETE_WINDOW', self.exit_app)
        #if os.path.isfile('images/beast.ico'): self.root.wm_iconbitmap('images/beast.ico')
        self.root.bind('<KeyPress>', self.key_pressed)
        self.root.bind('<KeyRelease>', self.key_released)
        self.root.mainloop()
        self.root.after(2000, after_startup)
        self.trackText = StringVar()

        #########PATTERN BUTTONS#################

    def create_top_bar(self):

        tabControls = []


        topbar_frame = Frame(self.root)
        topbar_frame.config(height=30)
        topbar_frame.grid_rowconfigure(3, minsize=20)
        topbar_frame.grid_columnconfigure(1, minsize=20)
        topbar_frame.grid(row=0, column=0, padx=10, sticky=W)

        note = ttk.Notebook(topbar_frame)

        self.pattBtnz = [0 for x in range(256)]

        for i in range(0, 8):
            mystr = str(i*32) + '-' + str((i*32)+32)

            thistab = ttk.Frame(note)
            tabControls.append(thistab)
            note.add(thistab, text=mystr)
            note.pack(expand=1, fill="both")
            self.monty = ttk.LabelFrame(thistab, text=mystr + "x")
            self.monty.grid(column=0, row=0, padx=8, pady=4)
            for j in range(i*32, (i*32)+32):
                pattStr = "patt" + str(j)
                self.pattBtnz[j] = Button(self.monty, name=pattStr, bg='white', activebackground='white',
                                          text=str(j + 1),
                                          width=self.btnW, height=self.btnH, command=self.patt_clicked(j))
                self.pattBtnz[j].grid(column=j%32, row=1)
                self.pattBtnz[j].bind('<Double-1>', self.pattDblClicked(j))
                self.pattBtnz[j].bind('<Control-Button-1>', self.pattCtrlClicked(j))

        self.units = IntVar()
        self.units.set(8)
        self.bpu = IntVar()
        self.bpu.set(4)
        print "outside loop now"
        self.createTimeLine()

    def create_top_barx(self):
        '''creating top buttons'''
        topbar_frame = Frame(self.root)
        topbar_frame.config(height=30)
        topbar_frame.grid_rowconfigure(3, minsize=20)
        topbar_frame.grid_columnconfigure(1, minsize=20)
        topbar_frame.grid(row=0, column=0, padx=20, sticky=W)

        self.pattBtnz = [0 for x in range(32)]

        for i in range(32):
            pattStr = "patt" + str(i)
            self.pattBtnz[i] = Button(topbar_frame, name=pattStr, bg='white', activebackground='white',
                                      text=str(i + 1),
                                      width=self.btnW, height=self.btnH, command=self.patt_clicked(i))
            self.pattBtnz[i].grid(row=0, column=i + 1)
            self.pattBtnz[i].bind('<Double-1>', self.pattDblClicked(i))
            self.pattBtnz[i].bind('<Control-Button-1>', self.pattCtrlClicked(i))

        btn_newPattern = Button(topbar_frame, name="btn_newPattern", bg='white', text="+", width=self.btnW,
                                height=self.btnH, command=self.newPattern())
        btn_newPattern.grid(row=0, column=i + 3, padx=10)

        self.units = IntVar()
        self.units.set(8)
        # self.units_widget = Spinbox(topbar_frame, from_=1, to=8, width=5, textvariable=self.units,
        #                             command=self.createTimeLine)
        # self.units_widget.grid(row=0, column=24)

        self.bpu = IntVar()
        self.bpu.set(4)
        # self.bpu_widget = Spinbox(topbar_frame, from_=1, to=10, width=5, textvariable=self.bpu,
        #                           command=self.createTimeLine)
        # self.bpu_widget.grid(row=0, column=26)

        self.createTimeLine()

        ######################MENUS#######################################
    def top_menu(self):
        self.menubar = Menu(self.root)

        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Load Project", command=self.load_project)
        self.filemenu.add_command(label="Save Project", command=self.save_project)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.exit_app)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.editmenu = Menu(self.menubar, tearoff=0)
        self.editmenu.add_command(label="Copy", command=self.copypattern)
        self.editmenu.add_command(label="Paste", command=self.pastepattern)
        self.editmenu.add_command(label="Add Bar Sequence", command=self.pastebarsequence)
        self.menubar.add_cascade(label="Edit", menu=self.editmenu)

        self.aboutmenu = Menu(self.menubar, tearoff=0)
        self.aboutmenu.add_command(label="About", command=self.about)
        self.aboutmenu.add_command(label="Settings", command=self.popupSettings)
        self.aboutmenu.add_command(label="New Song", command=self.newsong)
        self.aboutmenu.add_command(label="Edit Sequence", command=self.editSequence)
        self.aboutmenu.add_command(label="Delete Temporary Files", command=self.deleteTemporaryFiles)
        self.aboutmenu.add_command(label="Export Sequence",command=self.export_song)
        self.menubar.add_cascade(label="About", menu=self.aboutmenu)

        self.root.config(menu=self.menubar)

    #########################TIMELINE#####################


    def deleteTemporaryFiles(self):
        d = listfiles.FileListViewer(self.root)

    def createTimeLine(self):
        bpu = self.bpu.get()
        units = self.units.get()
        c = bpu * units
        right_frame = Frame(self.root)
        right_frame.grid(row=10, column=0, sticky=W + E + N + S, padx=15, pady=2)

        self.buttonrowz = [[0 for x in range(c)] for x in range(MAX_TRACK_NUM)]
        self.transbtnz = [0 for x in range(c)]
        self.startBtnz = [0 for x in range(c + 1)]
        self.stopBtnz = [0 for x in range(c + 1)]  # needs extra one because going up to 32
        self.drumpads = [None] * MAX_TRACK_NUM
        self.clearpads = [None] * MAX_TRACK_NUM

        # this creates the stop/start buttons
        Label(right_frame, text="Trunc").grid(row=0, column=0)
        for q in range(0, c):
            btnStartName = "btnStart" + str(q)
            btnName = "btnEnd" + str(q)
            f1 = Frame(right_frame)
            self.startBtnz[q] = Button(f1, name=btnStartName, bg='white', text=str(q + 1), width=self.btnW,
                                       height=self.btnH, command=self.start_clicked(q))
            self.stopBtnz[q] = Button(f1, name=btnName, bg='white', text=str(q + 1), width=self.btnW,
                                      height=self.btnH, command=self.stop_clicked(q + 1))
            self.startBtnz[q].grid(row=0, column=0)
            self.stopBtnz[q].grid(row=1, column=0)
            f1.grid(row=1, column=q)

        right_frame.grid_rowconfigure(1, minsize=20)

        Label(right_frame, text="Trans").grid(row=2, column=0)
        # these are the transpose buttons
        for q in range(c):
            btnName = "col" + str(q)
            numToShow = str(q % 12)
            self.transbtnz[q] = Button(right_frame, name=btnName, bg='white', text=numToShow, width=self.btnW,
                                       height=self.btnH, command=self.trans_clicked(q))
            self.transbtnz[q].grid(row=3, column=q)

        right_frame.grid_rowconfigure(2, minsize=20)
        row_base = 5
        Label(right_frame, text="Music").grid(row=4, column=0)
        for i in range(MAX_TRACK_NUM):
            self.makeTrackButtons(right_frame, i, row_base, c, bpu)

    def duplicateSequentialBars(self,fromBar,toBar,insertBar):
        ct=0
        currPatt = int(self.patt.get())
        if insertBar<toBar:
            return
        for i in range(fromBar,toBar+1):
            print "copying from " + str(fromBar+ct) + " to " + str(insertBar+ct)
            self.pattern_list[insertBar+ct-1] = copy.deepcopy(self.pattern_list[fromBar+ct-1])
            if i == currPatt:
                self.reconstruct_pattern(insertBar+ct-1, self.bpu.get(), self.units.get())
            ct = ct+1
        #check if any pattern is current - if so it needs to be reconstructed





    def makeTrackButtons(self, frameBase, rowNum, rowBase, maxBeats, beatsPerUnit):
        for j in range(maxBeats):

            self.active = False
            color = 'grey55' if (j / beatsPerUnit) % 2 else 'khaki'
            basscolor =  'grey88' if (j / beatsPerUnit) % 2 else 'lightpink'
            btnName = "btn" + str(rowNum) + ":" + str(j)
            if rowNum < 4:
                self.buttonrowz[rowNum][j] = Button(frameBase, name=btnName, bg=color, activebackground=color,
                                                    width=self.btnW, height=self.btnH,
                                                    command=self.button_clicked(rowNum, j, beatsPerUnit))
                # self.buttonrowz[i][j] = Button(right_frame, bg=color, width=1)
                self.buttonrowz[rowNum][j].bind('<Double-1>', self.percDblClicked)
            else:
                self.buttonrowz[rowNum][j] = Button(frameBase, bg=basscolor, activebackground=basscolor,
                                                    width=self.btnW, height=self.btnH)
                #                                   command=self.bass_clicked(rowNum, j, beatsPerUnit))
                self.buttonrowz[rowNum][j].bind("<ButtonPress-1>",
                                                lambda event, rn=rowNum, jay=j, BPU=beatsPerUnit: self.bass_clicked(
                                                    event, rn, jay, BPU))

            self.buttonrowz[rowNum][j].grid(row=rowNum + rowBase, column=j)

        drumPadName = "d_" + str(rowNum)
        self.drumpads[rowNum] = Button(frameBase, name=drumPadName, bg=color, width=self.btnW, height=self.btnH,
                                       command=self.d_clicked(drumPadName))
        frameBase.grid_columnconfigure(j + 1, minsize=10)
        self.drumpads[rowNum].grid(row=rowNum + rowBase, column=j + 2)

    def about(self):
        tkMessageBox.showinfo("About", "Tkinter GUI Application\n Development Hotshot")

    def key_pressed(self, event):
        c = repr(event.char)

    def key_released(self, event):

        if event.char in self.kbd:
            self.hitKey(self.kbdmappings[event.char],4)
            #print self.kbdmappings[event.char]

        if event.char == "z":
            self.hitDrum("_0")
        if event.char == 'x':
            self.hitDrum("_1")
        if event.char == 'c':
            self.hitDrum("_2")
        if event.char == 'v':
            self.hitDrum("_3")

    def exit_app(self):
        if tkMessageBox.askokcancel("Quit", "Do you really want to quit?"):
            self.root.destroy()

    def save_project(self):
        self.record_pattern()  # make sure the last pattern is recorded before save
        file_name = tkFileDialog.asksaveasfilename(filetypes=[('Drum Beat File', '*.bt')], title="Save project as...")
        with open(file_name, "wb") as f:

            pickle.dump(self.pattern_list, f)
            pickle.dump(self.trackText.get(),f)

        self.root.title(os.path.basename(file_name) + " - DrumBeast")

    def save_tmpfile(self):
        self.record_pattern()
        slash = os.path.sep
        #pathInQuestion = os.path.abspath(__file__)) . slash . "loops" . slash

        filename = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M.bt")
        filename = os.path.dirname(os.path.abspath(__file__)) + slash + "loops" + slash + filename

        #tkMessageBox.showinfo("Title", filename)

        pickle.dump(self.pattern_list, open(filename, "wb"))

    def load_project(self):
        file_name = tkFileDialog.askopenfilename(filetypes=[('Drum Beat File', '*.bt')], title='Load Project')
        self.setConfigValue("Settings","LastFile",file_name)

        self.read_file(file_name)



    def setConfigValue(self,section,key,value):
        myfolder = os.getcwd()
        configParser = ConfigParser.ConfigParser()
        fp = os.getcwd() + '/drummachine.config';

        configParser.read(fp)

        try:
            configParser.add_section(section)
        except:
            print "setting already exists"

        configParser.set(section, key, value)

        configfile = open(fp, 'w')
        configParser.write(configfile)
        configfile.close()

    def read_file(self,file_name):
        if file_name == '': return
        fh = open(file_name, "rb")  # open the file in reading mode
        try:
            self.pattern_list = pickle.load(fh)
            if self.trackText is None:
                self.trackText = StringVar()
            self.trackText.set(pickle.load(fh))
        except EOFError:
            pass
        fh.close()
        while len(self.pattern_list) < 32:
            self.pattern_list.append(None)
        try:
            self.reconstruct_pattern(0, self.pattern_list[0]['bpu'],
                                     self.pattern_list[0]['units'])  # reconstruct the first pattern
        except:
            tkMessageBox.showerror("Error", "An unexpected error occurred trying to reconstruct patterns")





    # essentially just records whatever is in the timeline and saves it to self.pattern_list at
    # the number it was before advancing to the current number (saved in self.prevpatvalue)
    # therefore working under the assumption that the new pattern is always one more than the previous one
    def record_pattern(self):
        if self.recordOnChange is False:
            return
        pattern_num, bpu, units = self.patt.get(), self.bpu.get(), self.units.get()

        print "recording", pattern_num

        c = bpu * units
        self.buttonpickleformat = [[0] * c for x in range(MAX_TRACK_NUM)]
        self.hitList = {}

        for i in range(MAX_TRACK_NUM):
            for j in range(c):
                if self.buttonrowz[i][j].config('bg')[-1] == 'green':
                    self.buttonpickleformat[i][j] = self.buttonrowz[i][j].cget('text')
                    self.hitList[self.buttonrowz[i][j]] = 1
                else:
                    self.buttonpickleformat[i][j] = ' '
        self.pattern_list[pattern_num] = {'df': self.widget_drum_file_name, 'bl': self.buttonpickleformat, 'bpu': bpu,
                                       'units': units}


        #self.reconstruct_pattern(pattern_num, bpu, units)

    # logics
    # DURING EDIT
    # 1) move from extant pattern to extant pattern: save, rinse, reconstruct, update
    # 2) move from extant to pasteable : save, update
    # 3) move from extant to new: save, rinse, update
    # DURING PLAY
    # 4) move from extant pattern to extant pattern: rinse, reconstruct, update

    def rec_pattern(self, currentPattNum):
        bpu = self.bpu.get()
        units = self.units.get()
        c = int(self.bpu.get()) * int(self.units.get())
        self.buttonpickleformat = [[0] * c for x in range(MAX_TRACK_NUM)]
        self.hitList = {}
        for i in range(MAX_TRACK_NUM):
            for j in range(c):
                if self.buttonrowz[i][j].config('bg')[-1] == 'green':
                    self.buttonpickleformat[i][j] = self.buttonrowz[i][j].cget('text')
                    self.hitList[self.buttonrowz[i][j]] = 1
                else:
                    self.buttonpickleformat[i][j] = ' '
        self.pattern_list[currentPattNum] = {'df': self.widget_drum_file_name, 'bl': self.buttonpickleformat,
                                             'bpu': bpu,
                                             'units': units}

    def goto_pattern(self, fromPattNum, toPattNum):
        if toPattNum > len(self.pattern_list): return
        self.currentPattern = toPattNum



    # def printTimeElapsed(self,msg):
    # currTime = time.clock()
    # print msg, currTime-self.prevTime
    # self.prevTime=currTime

    def paste_pattern(self, pattern_num, bpu, units):
        print "Reconstructing"
        self.prevTime = time.clock()

        c = bpu * units

        # self.rinseTimeline(c,bpu)
        try:
            for i in range(MAX_TRACK_NUM):
                for j in range(c):
                    # if self.pattern_list[pattern_num]['bl'][i][j] == '*':
                    toPlay = self.pattern_list[pattern_num]['bl'][i][j]
                    if len(toPlay) > 0 and toPlay != " ":
                        self.buttonrowz[i][j].config(bg='green', text=toPlay)
        except:
            return

        return time.clock() - self.prevTime




    def pattern_to_ascii(self,pattern_num,startAt=0,stopAt=32,transpose=0):
        retval=""
        for i in range(MAX_TRACK_NUM - 1):
            for j in range(startAt,stopAt):
                note = self.pattern_list[pattern_num]['bl'][i][j]
                if len(note) > 0 and note != " ":
                    retval=retval+self.resolveMidiNum(note,transpose,i)+","
                else:
                    retval = retval+","
        retval = re.sub(r'^,,*$', '', retval)
        while "\n\n" in retval:
            retval.replace("\n\n","\n")
        retval = retval.strip()



        return retval

    def pattern_to_ascii_beat_by_beat(self,pattern_num,startAt=0,stopAt=32,transpose=0):
        retval=""
        for j in range(startAt, stopAt):
            for i in range(MAX_TRACK_NUM - 1):
                note = self.pattern_list[pattern_num]['bl'][i][j]
                if len(note) > 0 and note != " ":
                    retval=retval+self.resolveMidiNum(note,transpose,i)+","
                else:
                    retval = retval+","
            retval=retval+"\n"
        return retval

    def pattern_to_ascii_beat_by_beat_arr(self,pattern_num,startAt=0,stopAt=32,transpose=0):
        retval=[]
        for j in range(startAt, stopAt):
            for i in range(MAX_TRACK_NUM - 1):
                notes_at_beat_arr = []
                note = self.pattern_list[pattern_num]['bl'][i][j]
                if len(note) > 0 and note != " ":
                    notes_at_beat_arr.append(self.resolveMidiNum(note,transpose,i))
                else:
                    notes_at_beat_arr.append('')
            retval.append(notes_at_beat_arr)
        return retval

    def resolveMidiNum(self,note,transpose,track):
        if note=="*":
            return str(track+36)
        else:
            return str(self.keyNumz[note])

    def export_song(self):
        allbars = self.breaks_to_ascii_barlist()
        print allbars
        m = MidiWriter.midWriter()
        m.writeSong(allbars)
        #m.writeScale()



    def breaks_to_ascii(self):
        retval = ""
        ct=0
        mysong = song.Song()
        self.breaks = mysong.getSequenceArray(self.trackText.get())
        for breaky in self.breaks:
            retval=retval+self.pattern_to_ascii(breaky.pattern,breaky.startAt,breaky.stopAt,breaky.transpose)+"\n"
            ct=ct+1
        print retval
        return retval;

    def breaks_to_ascii_barlist(self):
        retval = ""
        ct = 0
        mysong = song.Song()
        self.breaks = mysong.getSequenceArray(self.trackText.get())
        for breaky in self.breaks:
            retval = retval + (self.pattern_to_ascii_beat_by_beat(breaky.pattern,breaky.startAt,breaky.stopAt,breaky.transpose)) + "\n"
        while "\n\n" in retval:
            retval = retval.replace("\n\n","\n")
        return retval.strip()


    def append_string_line_by_line(self, stringa, stringb):
        retval = ""
        lista = stringa.split("\n")
        listb = stringa.split("\n")
        ct=0
        for ln in lista:
            retval=retval+ln+listb[ct] + "\n"
            ct=ct+1
        return retval

    def merge_ascii_bars(self,barlist):
        retval = ""
        barstrings = []
        for barstring in barlist:
            barlines = barstring.split("\n")
            barstrings.append(barlines)
        for i in range(6):
            for barlinearray in barstrings:
                retval=retval+barlinearray[i]
            retval = retval+"\n"
        return retval

    def makeNotesAtTimePointArray(self,ascii_string):
        lis = [x.replace('\n', '').split(',') for x in ascii_string]
        for x in zip(*lis):
            for y in x:
                print(y + ', ')
            print('')




    def reconstruct_pattern(self, pattern_num, bpu, units, rinse=True):

        print "reconstructing",pattern_num

        self.prevTime = time.clock()

        c = bpu * units

        if rinse:
            self.rinseTimeline()
            self.hitList = {}
            try:
                for i in range(MAX_TRACK_NUM-1):
                    for j in range(c):
                        # if self.pattern_list[pattern_num]['bl'][i][j] == '*':
                        toPlay = self.pattern_list[pattern_num]['bl'][i][j]
                        if len(toPlay) > 0 and toPlay != " ":
                            self.buttonrowz[i][j].config(bg='green', text=toPlay)
                            self.hitList[self.buttonrowz[i][j]] = 1
            except Exception as e:
                print (e)
                return 0

        return time.clock() - self.prevTime


    def play_in_thread_once(self):
        self.loop=False
        self.setSeq(False)

        self.play_in_thread()


    def play_in_thread_looped(self):
        self.loop=True
        self.setSeq(False)
        self.play_in_thread()

    def play_in_thread_seq(self):

        self.loop=True
        self.setSeq(True)
        mysong = song.Song()
        self.breaks = mysong.getSequenceArray(self.trackText.get())
        print mysong
        print self.breaks
        self.play_in_thread()


    def play_in_thread(self):
        # print "About to play ",self.percPort, self.bassPort
        self.save_tmpfile()
        #self.pattBtnz[self.patt.get()].config(bg='turquoise')
        self.thread = threading.Thread(None, self.play, None, (), {})
        self.thread.start()


    def write(self):
        self.startAt = int(self.breaks[0].startAt)
        self.stopAt = int(self.breaks[0].stopAt)
        self.transpose = int(self.breaks[0].transpose)
        self.reconstruct_pattern(int(self.breaks[0].pattern), self.bpu.get(), self.units.get())


    def play(self):
        ct = 0
        self.startAt = 0
        self.stopAt = len(self.buttonrowz[0])
        self.thetime = time.time()
        self.keep_playing = True
        endMeasure = self.units.get() * self.bpu.get()



        if self.seq==True:
            print "breaks is " + str(self.breaks[0].pattern)
            self.startAt = int(self.breaks[0].startAt)
            self.stopAt = int(self.breaks[0].stopAt)
            self.transpose = int(self.breaks[0].transpose)
            self.reconstruct_pattern(int(self.breaks[0].pattern), self.bpu.get(),self.units.get())

        while self.keep_playing:
            # self.button is an an array of button rows

            # going through all the measures one by one

            for i in range(self.startAt,self.stopAt):

                reconstruction_delay = 0
                self.stopBtnz[i].config(bg='green')
                if i > 0:
                    self.stopBtnz[i - 1].config(bg='white')
                else:
                    self.stopBtnz[self.stopAt - 1].config(bg='white')

                # at each measure proceeding vertically down

                for thisrow in self.buttonrowz:

                    currentButton = thisrow[i]
                    currentRowNumber = self.buttonrowz.index(thisrow)
                    try:
                        if currentButton.cget('bg') == 'green':
                            if currentRowNumber < 4:
                                self.play_drum(self.channels[currentRowNumber].inst_or_note,self.channels[currentRowNumber].channel)
                            else:
                                note_to_play = currentButton['text']
                                if note_to_play != "":
                                    self.play_note(self.channels[currentRowNumber].inst_or_note,self.keyNumz[note_to_play], self.channels[currentRowNumber].channel)

                    except Exception as e:
                        print "exception at ", i, str(e)
                        continue


                reconstruction_delay = 0
                #this deals with what happens in the last beat (is new pattern added or not
                if i == self.stopAt - 1:


                    if self.seq==False and self.loop==True:#i.e we are in play looped mode
                        if self.queuedPattern != self.patt.get(): #and the next pattern is not the same as the current one
                            self.record_pattern()                                      #save current pattern if need to
                            self.patt.set(self.queuedPattern)
                            reconstruction_delay = self.reconstruct_pattern(self.queuedPattern, self.bpu.get(),
                                                                            self.units.get())

                    else:

                        if ct >= len(self.breaks)-1:
                            ct=-1
                        upcoming = self.breaks[ct+1]

                        if upcoming.pattern !=self.breaks[ct].pattern:
                            reconstruction_delay = self.reconstruct_pattern(int(upcoming.pattern), self.bpu.get(),
                                                                            self.units.get())
                        self.startAt = upcoming.startAt
                        self.stopAt = upcoming.stopAt
                        self.transpose = upcoming.transpose

                    ct = ct + 1
                    #print "ct now is", ct, " of ", len(self.breaks), self.breaks[ct].pattern
                print self.bpm,reconstruction_delay
                bpm_based_delay = max(((60.0 / self.bpm) / 4.0) - reconstruction_delay, 0)

                time.sleep(bpm_based_delay)
                self.end_notes()
                self.currNote = i
                self.thetime = time.time()

                if self.loop==False:  self.keep_playing = False
        #after loop finishes
        if (self.seq==False):
            self.patt.set(self.currentPattern)
        else:
            self.seq=False
            self.patt.set(-1)



    def row_to_drum_num(self, rownum):
        return self.channels[rownum].channel

    def play_drum(self, num, ch):
        self.midi_out.set_instrument(50, channel=ch)
        self.midi_out.note_on(num, 127, ch)
        self.notesOn.append((num, ch))

    def play_note(self, inst, note, ch):
        note = note + self.transpose
        self.midi_out.set_instrument(inst, channel=ch)
        self.midi_out.note_on(note, 127, ch)
        self.notesOn.append((note, ch))

    def playDemoInstrument(self,inst):
        def callback():
            print inst
            self.midi_out.set_instrument(inst, 15)
            self.midi_out.note_on(50, 127, 15)
            time.sleep( 1 )
            self.midi_out.note_off(50, 127, 15)
        return callback

    def playDemoDrum(self,note):
        def callback():
            print note
            self.midi_out.note_on(note, 127, 9)
            time.sleep( 1 )
            self.midi_out.note_off(note, 127, 9)
        return callback


    def end_notes(self):
        for note in self.notesOn:
            self.midi_out.note_off(note[0], 0, note[1])
        self.notesOn = []

    def stop_play(self):
        self.keep_playing = False
        self.loop=False
        self.seq=False

        return

    def enablePatterns(self):
        for i in range(len(self.pattBtnz)):
            self.pattBtnz[i].config(state='normal')

    def disablePatterns(self):
        for i in range(len(self.pattBtnz)):
            self.pattBtnz[i].config(state='disabled')


    def setSeq(self,val):
        self.seq=val
        print "in setSeq",len(self.pattBtnz)
        if val==False:
            self.enablePatterns()
        else:
            self.disablePatterns()


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

        self.addToDrumWidget(file_name, drum_no)

        print self.dict

    def addToDrumWidget(self, drum_name, drum_no):
        return
        # basically this is clearing and filling  a text box
        # self.widget_drum_name[drum_no].delete(0, END)
        # self.widget_drum_name[drum_no].insert(0, drum_name)
        # print "inserting this", self.widget_drum_name[drum_no]

    def drum_load(self, drum_no):
        def callback():
            self.current_drum_no = drum_no
            try:
                file_name = tkFileDialog.askopenfilename(defaultextension=".wav",
                                                         filetypes=[("Wave Files", "*.wav"), ("OGG Files", "*.ogg")])
                if not file_name: return
                print file_name, drum_no
                self.addFileToDrumset(file_name, drum_no)

            except:
                tkMessageBox.showerror('Invalid', "Error loading drum samples")

        return callback

    def bass_load(self, drum_no, note):
        def callback():
            pth = os.path.dirname(os.path.realpath(__file__))
            file_name = pth + "\\notes\\" + note + ".wav"
            self.current_drum_no = drum_no
            try:
                if not file_name: return
                print file_name, drum_no
                self.addFileToDrumset(file_name, drum_no)

            except:
                tkMessageBox.showerror('Invalid', "Error loading drum samples")

        return callback

    def button_clicked(self, i, j, bpu):
        def callback():
            self.change_beat(i, j, bpu)

        return callback

    def change_beat(self, i, j, bpu):
        btn = self.buttonrowz[i][j]
        color = 'grey55' if (j / bpu) % 2 else 'khaki'
        txt = ' '
        new_color = 'green' if btn.cget('bg') != 'green' else color
        new_text = '*' if (btn.cget('text') == '' or btn.cget('text') == ' ') else txt
        btn.config(bg=new_color)
        btn.config(text=new_text)

    def insert_beat(self, i, j, bpu):
        btn = self.buttonrowz[i][j]
        color = 'grey55' if (j / bpu) % 2 else 'khaki'
        txt = ' '
        new_color = 'green'
        new_text = '*'
        btn.config(bg=new_color)
        btn.config(text=new_text)


    def rinseTimelineOld(self, numCols, bpu):
        for i in range(MAX_TRACK_NUM):
            for j in range(numCols):
                color = 'grey55' if (j / bpu) % 2 else 'khaki'
                self.buttonrowz[i][j].config(text=' ', bg=color)
                # self.buttonrowz[i][j].config(bg=color)

    def rinseTimeline(self):
        for btn in self.hitList:
            color = btn.cget('activebackground')
            btn.config(text=' ', bg=color)

    def bass_clicked(self, event, i, j, bpu):
        btn = self.buttonrowz[i][j]
        color = 'lightpink'
        if btn.cget('bg') != 'green':
            piano.Piano(self, btn,i)
            new_color = 'green'
            self.addToDrumWidget("piano", 4)
        else:
            new_color = color
            btn.config(text="")
        btn.config(bg=new_color)

    def create_play_bar(self):
        playbar_frame = Frame(self.root, height=15)
        ln = MAX_TRACK_NUM + 10
        playbar_frame.grid(row=ln, columnspan=20, sticky=W + E, padx=15, pady=10)

        button = ttk.Button(playbar_frame, text='Play', command=self.play_in_thread)
        button.grid(row=ln, column=1, padx=1)

        btnPlayLooped = ttk.Button(playbar_frame, text='Play Looped', command=self.play_in_thread_looped)
        btnPlayLooped.grid(row=ln, column=2, padx=1)

        btnPlaySeq = ttk.Button(playbar_frame, text='Play Seq', command=self.play_in_thread_seq)
        btnPlaySeq.grid(row=ln, column=3, padx=1)

        button = ttk.Button(playbar_frame, text='Stop', command=self.stop_play)
        button.grid(row=ln, column=4, padx=1)


        # loop = BooleanVar()
        # loopbutton = ttk.Checkbutton(playbar_frame, text='Loop', variable=loop,
        #                              command=lambda: self.loop_play(loop.get()))
        # loopbutton.grid(row=ln, column=16, padx=1)
        #
        # play_seq = BooleanVar()
        # btn_play_seq = ttk.Checkbutton(playbar_frame, text='Sequence', variable=loop,
        #                                command=lambda: self.sequence_play(play_seq.get()))
        # btn_play_seq.grid(row=ln, column=18, padx=1)

        Label(playbar_frame, text='BPM:').grid(row=ln, column=20, padx=30)
        self.bpmTxt = StringVar()
        self.bpmTxt.set(120)
        Spinbox(playbar_frame, from_=80, to=160, width=5, textvariable=self.bpmTxt).grid(row=ln,column=21)

        Label(playbar_frame, text='Pattern #:').grid(row=ln, column=22)
        self.patt = IntVar()
        self.patt.set(0)
        self.prevpatvalue = 0  # to trace last click
        Spinbox(playbar_frame, from_=0, to=32, width=10, textvariable=self.patt, command=self.record_pattern).grid(row=ln,
                                                                                                                  column=23)

        self.pat_name = Entry(playbar_frame)

        self.pat_name.grid(row=ln, column=24, padx=1, pady=1)
        self.pat_name.insert(0, 'Pattern %s' % self.patt.get())
        self.pat_name.config(state='readonly', width=10)



        #self.bpu_widget = Spinbox(playbar_frame, from_=80, to=160, width=5, textvariable=self.bpmTxt,
        #                          command=self.changeBpm)
        #self.bpu_widget.grid(row=ln, column=21)

        self.recordWhileLooping = IntVar()
        Checkbutton(playbar_frame, text="Record While Looping", variable=self.recordWhileLooping).grid(row=ln,column=24)

        Label(playbar_frame, text='Sequence Text:').grid(row=ln, column=25, sticky=W)
        self.formula = StringVar()
        txtformula = Entry(playbar_frame, textvariable=self.formula, width=60)
        txtformula.grid(row=ln, column=26, columnspan=1, sticky=W)

        self.seqBtn = Button(playbar_frame, name="seqBtn", text="Run Sequence", command=self.run_sequence)
        self.seqBtn.grid(row=ln, column=25)

        self.diagnosticsLabel = Label(playbar_frame, text='diagnostics').grid(row=ln, column=30, sticky=W)

        # playbar_frame.bind("<Key>", self.quay)

    def run_sequence(self):

        mysong = song.Song()
        theseq = mysong.getSequenceArray(self.formula.get())


    def quay(self, event):
        print "pressed"

    def percValue(self, value):
        portId = self.deviceDict[value]
        print "The port is ", portId
        self.percPort = portId
        print value, portId
        self.setConfigValue("Settings", "PortId", portId)
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
        left_frame.grid(row=10, column=0, columnspan=6, sticky=W + E + N + S)
        tbicon = PhotoImage(file='images/openfile.gif')
        for i in range(0, MAX_TRACK_NUM):
            button = Button(left_frame, image=tbicon, command=self.drum_load(i))
            button.image = tbicon
            button.grid(row=i, column=0, padx=5, pady=2)
            self.drum_entry = Entry(left_frame)
            self.drum_entry.grid(row=i, column=4, padx=7, pady=2)
            self.widget_drum_name.append(self.drum_entry)



    def trans_clicked(self, num):
        def callback():
            self.transpose = num
            print "self transpose is now ", self.transpose
            self.trans_rinse()
            self.transbtnz[num].config(bg="sky blue")

        return callback

    def start_clicked(self, num):
        def callback():
            self.startAt = num
            print "self startAt is now ", self.startAt
            self.start_rinse()
            self.startBtnz[num - 1].config(bg="sky blue")

        return callback

    def stop_clicked(self, num):
        def callback():
            self.stopAt = num
            print "self numMeasures is now ", self.stopAt
            self.stop_rinse()
            self.stopBtnz[num - 1].config(bg="sky blue")

        return callback

    def trans_rinse(self):
        for j in range(32):
            self.transbtnz[j].config(bg="White")

    def start_rinse(self):
        for j in range(32):
            self.startBtnz[j].config(bg="White")

    def stop_rinse(self):
        for j in range(32):
            self.stopBtnz[j].config(bg="White")

    def pattShow(self):
        for j in range(32):
            if int(self.patt.get())==j:
                self.pattBtnz[j].config(bg="turquoise")
            elif self.pattern_list[j]==None:
                self.pattBtnz[j].config(bg="White")
            else:
                self.pattBtnz[j].config(bg="Pink")

    def pattCtrlClicked(self, num):
        if self.loop != False and self.keep_playing != False:
            self.saveWhileLooping=True
            self.queuedPattern = int(num)


    def patt_clicked(self, num):

        #here is the button for changing patterns
        #for simplicity's sake here -
        #during looping: changes saved if control button clicked in the source pattern, and the pattern reloaded in the destination pattern
        #during no looping, saves done automatically
        #during sequence playing no saving allowed
        #however this merely queues the next pattern
        #the actually
        def callback():

            #self.diagnosticsLabel.text="self.loop=" + str(self.loop) + " self.keep_playing=" + str(self.keep_playing) + " self.seq=" + str(self.seq)

            if self.seq:
                print "in seq"
                return

            self.queuedPattern = int(num)

            if self.loop != False and self.keep_playing != False:
                #we are running

                self.pattBtnz[self.queuedPattern].config(bg='yellow')
                print "self pattQueued is now ", self.queuedPattern #saving storing and reanimating done by the play function
            else:

                #immediately after a stop = self.patt.set should be to the current pattern
                self.prevpatvalue = self.patt.get()
                self.record_pattern()
                self.patt.set(int(num))
                self.reconstruct_pattern(int(num), self.bpu.get(), self.units.get())
                self.pattShow()

        return callback

    def d_clicked(self, dname):
        def callback():
            print dname
            if self.loop != False and self.keep_playing != False:
                self.hitDrum(dname)
            else:
                self.setChannelValues(dname)

        return callback

    def setChannelValues(self, dname):

        rowclicked = int(dname.split("_")[1])
        self.channels[rowclicked].init_user_interface(rowclicked)

    def hitDrum(self, dname):
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

    def hitKey(self, note, rowclicked):

        delay = (60.0 / self.bpm) / 4.0
        timesincenotechange = time.time() - self.thetime
        rowclicked = int(rowclicked)

        notepos = self.currNote
        if (timesincenotechange / delay > 0.5):
            self.buttonrowz[rowclicked][notepos].config(bg='green')
            self.buttonrowz[rowclicked][notepos].config(text=note)
        else:
            notepos = notepos - 1
            if notepos < 0: notepos = 31
            self.buttonrowz[rowclicked][notepos].config(bg='green')
            self.buttonrowz[rowclicked][notepos].config(text=note)



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

        for i in range(1, 5):
            Label(popup, text="Drum" + str(i)).grid(row=i, column=0)

        popup.title("Major Settings")
        popup.configure(background="#d9d9d9")
        popup.wm_title("!")
        popup.mainloop()

    def del_clicked(self, xname):
        print xname

    def percDblClicked(self, event):
        a = str(event.widget).split(".")[-1]
        rw = a[3:].split(":")[0]
        cl = a[3:].split(":")[1]
        print rw
        print cl
        self.popupmsg(str(rw) + ":" + str(cl))

    def pattDblClicked(self, num):
        print num
        # a = str(event.widget).split(".")[-1]
        # a = a[4:]
        # print a
        # thelen = len(self.pattern_list)
        # self.record_pattern()
        # currPattern = self.pattern_list[int(a)]
        # copiedPattern = copy.deepcopy(currPattern)
        # self.pattern_list.append(copiedPattern)

    def popupmsg(self, msg):

        popup = Toplevel(self.root)
        popup.geometry("302x115+645+237")
        popup.title("Add Beats")
        popup.configure(background="#d9d9d9")
        popup.wm_title("!")
        self.btn = [None] * 5
        btnXpos = 0.17
        for i in range(5):
            btnName = "beats" + str(i)
            self.btn[i] = Button(popup, name=btnName,
                                 command=lambda name=str(int(math.pow(2, i + 1))): self.add_beats(name,
                                                                                                  msg) and popup.destroy())
            self.btn[i].place(relx=btnXpos, rely=0.43, height=25, width=37)
            self.btn[i].configure(pady="0")
            self.btn[i].configure(text=str(int(math.pow(2, i + 1))))
            btnXpos = btnXpos + 0.13

        label = ttk.Label(popup, text=msg)
        label.pack(side="top", fill="x", pady=10)
        B1 = ttk.Button(popup, text="Cancel", command=popup.destroy)
        B1.place(relx=0.40, rely=0.70, height=25, width=50)
        popup.mainloop()

    def add_beats(self, num, msg):
        row = int(msg.split(':')[0])
        col = int(msg.split(':')[1])
        r = row
        c = col
        while col < 32:
            # self.buttonrowz[row][col].config(bg='green')
            self.change_beat(row, col, self.bpu.get())
            col = col + int(num)
        self.insert_beat(r, c, self.bpu.get())
        return True

    def remove_beats(self, num, frm,to):
        for j in range(frm-1,to):
            origCol = self.buttonrowz[num][j].cget('activebackground')
            self.buttonrowz[num][j].config(bg=origCol)
            self.buttonrowz[num][j].config(text='')

    def CopyTrack(self, num, frm,to):
        self.clipboardTrack = []
        for j in range(frm-1,to):
            self.clipboardTrack.append(self.buttonrowz[num][j].cget('text'))

    def PasteTrack(self, num, frm, to):
        toPaste = []
        toPaste.extend(self.clipboardTrack)
        while len(toPaste) <32: toPaste.extend(self.clipboardTrack)
        for j in range(frm - 1, to):
            origCol = self.buttonrowz[num][j].cget('activebackground')
            toAddAtBeat = toPaste[j]
            self.buttonrowz[num][j].config(text=toAddAtBeat)
            if toAddAtBeat=='':self.buttonrowz[num][j].config(bg=origCol)
            else:self.buttonrowz[num][j].config(bg='green')

    def DuplicateTrackSection(self, num, frm, to):
        self.CopyTrack(frm,to)
        self.PasteTrack(to+1,32)

    def permTranspose (self, num, frm, to, offset):
        for j in range(frm - 1, to):
            origNote = self.buttonrowz[num][j].cget('text')
            if len(origNote)>0:
                print origNote
                pos = self.notes.index(origNote)
                newKey = self.notes[pos+offset]
                self.buttonrowz[num][j].config(text=newKey)



    def newPattern(self):
        def callback():
            self.prevpatvalue = self.patt.get()
            self.patt.set(len(filter(None, self.pattern_list)))
            # self.paste_pattern(self.patt.get(),self.bpu.get(),self.units.get())

        return callback

    def pastebarsequence(self):
        d = copybars.BarCopier(self.root,self)

    def copypattern(self):
        self.patternToCopy = int(self.patt.get())

    def pastepattern(self):
        result = tkMessageBox.askquestion("Pasting Will Overwrite!", "Are You Sure?", icon='warning')
        if result == 'yes':
            if self.patternToCopy!=-1:
                self.reconstruct_pattern(self.patternToCopy,self.bpu.get(), self.units.get())
                self.patternToCopy=-1
            else:
                tkMessageBox("No pattern copied")



    def newsong(self):
        nsd = newsongdlg.NewSongDialog(self)
        nsd.init_user_interface()

    def editSequence(self):
        if self.trackText is None:
            self.trackText = StringVar()
        self.ed.init_ui()

    def after_startup(self):
        print "whatever"



    def after_startup(self):
        print "hello"

    def key(event):
        print "pressed", repr(event.char)

    def _print_device_info(self):
        for i in range(pygame.midi.get_count()):
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
        for i in range(pygame.midi.get_count()):
            r = pygame.midi.get_device_info(i)
            (interf, name, input, output, opened) = r

            in_out = ""
            if input:
                in_out = "(input)"
            if output:
                in_out = "(output)"

            s = "{}: interface :{}:, name :{}:, opened :{}:  {}".format(i, interf, name, opened, in_out)
            mydict[s] = i
        return mydict




class soundThing():
    def __init__(self, pgmixer, fn, ch):
        self.filename = fn
        self.channelNumber = ch
        self.pyGameMixer = pgmixer
        self.snd = pgmixer.Sound(fn)

    def play(self):
        self.pyGameMixer.Channel(self.channelNumber).play(self.snd)


# ======================================================================
if __name__ == '__main__':


    w=3
    h=3
    print len(sys.argv)

    if (len(sys.argv)==3):
        w=int(sys.argv[1])
        h=int(sys.argv[2])

    dm = DrumMachine(w,h)


    dm.app()

