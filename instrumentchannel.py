from Tkinter import *
import ttk
import tkFileDialog
import tkMessageBox
import math
import os
import time
import piano

#modules for playing sounds
import time
import wave

import threading
import pickle

import ttk

import pygame
import pygame.midi
import math
import ConfigParser

from idlelib.ToolTip import *

from random import randint






class InstrumentChannel:



    def __init__(self,parentself,i,v,c):
        self.inst_or_note = i
        self.velocity = v
        self.channel = c
        self.parent = parentself
        self.currRow=0
        self.clmct=0

        config = ConfigParser.RawConfigParser()
        config.read('config.txt')

        self.details_dict = dict(config.items('instruments'))





    def clm(self):
        self.clmct+=1
        return self.clmct

    def clm0(self):
        self.clmct=0

    def init_user_interface(self,rowNum):
        #rowNum is just a temporary value so the UI knows which row has been chosen
        self.top = Toplevel(self.parent.root)
        self.top.geometry('1200x200')
        self.currRow = rowNum


        note = ttk.Notebook(self.top)



        noteFrame = ttk.Frame(note)

        note.add(noteFrame, text="Track Operations")
        note.pack(expand=1, fill="both")
        #note.pack(expand=1, fill="both")
        #tabControls.append(noteFrame)

        monty = ttk.LabelFrame(noteFrame, text="Track Operations")
        monty.grid(column=0, row=0, padx=8, pady=4)

        Label(monty, text="Settings").grid(row=0, column=self.clm())

        Label(monty, text="Inst/Note").grid(row=0,column=self.clm())
        self.txtInstrument = Entry(monty)
        self.txtInstrument.insert(END, str(self.inst_or_note))
        self.txtInstrument.grid(row=0, column=self.clm())

        Label(monty, text="Channel").grid(row=0,column=self.clm())
        self.txtChannel = Entry(monty)
        self.txtChannel.insert(END,str(self.channel))
        self.txtChannel.grid(row=0, column=self.clm())

        Label(monty, text="Velocity").grid(row=0,column=self.clm())
        self.txtVelocity = Entry(monty)
        self.txtVelocity.insert(END,str(self.velocity))
        self.txtVelocity.grid(row=0, column=self.clm())

        muteButton = Button(monty, text="Mute", command=self.btnMuteUnmute)
        muteButton.grid(row=0, column=self.clm())

        self.clm0()

        #s = Separator(monty, orient=VERTICAL).grid(column=0, row=0, rowspan=10, sticky='ns')

        ttk.Separator(monty, orient='horizontal').grid(column=0, row=1, rowspan=10, sticky='ew')


        self.clm()

        Label(monty, text="Track").grid(row=2, column=self.clm())

        copyButton = Button(monty, text="Copy", command=self.btnCopyTrack)
        copyButton.grid(row=2, column=self.clm())

        pasteButton = Button(monty, text="Paste", command=self.btnPasteTrack)
        pasteButton.grid(row=2, column=self.clm())

        duplicateButton = Button(monty, text="Duplicate", command=self.btnDuplicateTrackSection)
        duplicateButton.grid(row=2, column=self.clm())

        transposeButton = Button(monty, text="Transpose", command=self.doPermanentTransposition)
        transposeButton.grid(row=2, column=self.clm())

        self.transposeOffset = StringVar()
        self.transposeOffset.set('0')  # set the default option
        transposeOffsetDropDown = OptionMenu(monty, self.transposeOffset, 0,1,2,3,4,5,6,7,8,9,10,11,12)
        transposeOffsetDropDown.grid(row=2, column=self.clm())

        deleteButton = Button(monty, text="Delete Notes", command=self.delNotes)
        deleteButton.grid(row=2, column=self.clm())

        Label(monty, text="From").grid(row=2, column=self.clm())

        self.defaultFrom = StringVar()
        self.defaultFrom.set('1')  # set the default option
        fromDropDown= OptionMenu(monty, self.defaultFrom,1, 4, 9,13,17, 21,25,29)
        fromDropDown.grid(row=2, column=self.clm())

        Label(monty, text="To").grid(row=2, column=self.clm())

        self.defaultTo = StringVar()
        self.defaultTo.set('32')  # set the default option
        toDropDown = OptionMenu(monty, self.defaultTo, 4, 8, 12, 16, 20, 24, 28,32)
        toDropDown.grid(row=2, column=self.clm())

        self.clm0()




        b = Button(monty, text="OK", command=self.ok)
        b.grid(row=3, column=self.clm())

        c = Button(monty, text="Cancel", command=self.cancel)
        c.grid(row=3, column=self.clm())

        r= Button(monty, text="Record", command=self.recordPopup)
        r.grid(row=4, column=self.clm())

        noteFrame2 = ttk.Frame(note)

        note.add(noteFrame2, text="Voice Chooser")
        note.pack(expand=1, fill="both")

        monty2 = ttk.LabelFrame(noteFrame2, text="Choose Voice")
        monty2.grid(column=0, row=0, padx=8, pady=4)

        colors = []
        fcolors = []

        for i in range(16):
            intcol = randint(0, 0xFFFFFF)
            c = '%06X' % intcol
            f = 0xFFFFFF-intcol
            colors.append(c)
            fcolors.append('%06X' % f)

        for i in range(4):
            for j in range(32):
                total=i*32+j
                col="#" + str(colors[int(math.floor(total/8))])
                fcol = "#" + str(fcolors[int(math.floor(total/8))])
                btn = Button(monty2, text=str(total+1), width=3,fg=fcol,bg=col,command=self.parent.playDemoInstrument(total))
                btn.grid(column=j, row=i)
                igroupbasenum= int(math.floor(total/8))
                inststoshow = []
                for q in range(total,total+8):
                    if q>127:
                        continue
                    inststoshow.append(str(q+1) + " " + self.details_dict[str(q+1)])

                tip = ListboxToolTip(btn, inststoshow)



    def recordPopup(self):
        noteFrame.destroy()
        piano.Piano(self.parent, None,self.currRow)
        self.parent.play_in_thread_looped()


    def ok(self):
        self.inst_or_note = int(self.txtInstrument.get())
        self.channel = int(self.txtChannel.get())
        self.velocity = int(self.txtVelocity.get())
        noteFrame.destroy()

    def cancel(self):
        noteFrame.destroy()

    def delNotes(self):

        self.parent.remove_beats(self.currRow,int(self.defaultFrom.get()),int(self.defaultTo.get()))


    def btnMuteUnmute(self):
        self.parent.MuteUnMute(self.currRow)


    def btnCopyTrack(self):
        self.parent.CopyTrack(self.currRow,int(self.defaultFrom.get()),int(self.defaultTo.get()))


    def btnPasteTrack(self):
        self.parent.PasteTrack(self.currRow,int(self.defaultFrom.get()),int(self.defaultTo.get()))


    def btnDuplicateTrackSection(self):
        self.parent.DuplicateTrackSection(self.currRow, int(self.defaultFrom.get()), int(self.defaultTo.get()))

    def doPermanentTransposition(self):
        self.parent.permTranspose(self.currRow, int(self.defaultFrom.get()), int(self.defaultTo.get()), int(self.transposeOffset.get()))
