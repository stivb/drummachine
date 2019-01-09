from Tkinter import *
import ttk
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





class InstrumentChannel:



    def __init__(self,parentself,i,v,c):
        self.instrument = i
        self.velocity = v
        self.channel = c
        self.parent = parentself
        self.currRow=0
        self.clmct=0


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



        Label(self.top, text="Settings").grid(row=0, column=self.clm())

        Label(self.top, text="Instrument").grid(row=0, column=self.clm())
        self.txtInstrument = Entry(self.top)
        self.txtInstrument.insert(END, str(self.instrument))
        self.txtInstrument.grid(row=0, column=self.clm())

        Label(self.top, text="Instrument").grid(row=0,column=self.clm())
        self.txtInstrument = Entry(self.top)
        self.txtInstrument.insert(END,str(self.instrument))
        self.txtInstrument.grid(row=0, column=self.clm())

        Label(self.top, text="Channel").grid(row=0,column=self.clm())
        self.txtChannel = Entry(self.top)
        self.txtChannel.insert(END,str(self.channel))
        self.txtChannel.grid(row=0, column=self.clm())

        Label(self.top, text="Velocity").grid(row=0,column=self.clm())
        self.txtVelocity = Entry(self.top)
        self.txtVelocity.insert(END,str(self.velocity))
        self.txtVelocity.grid(row=0, column=self.clm())

        muteButton = Button(self.top, text="Mute", command=self.btnMuteUnmute)
        muteButton.grid(row=0, column=self.clm())

        self.clm0()

        #s = Separator(self.top, orient=VERTICAL).grid(column=0, row=0, rowspan=10, sticky='ns')

        ttk.Separator(self.top, orient='horizontal').grid(column=0, row=1, rowspan=10, sticky='ew')


        self.clm()

        Label(self.top, text="Track").grid(row=2, column=self.clm())

        copyButton = Button(self.top, text="Copy", command=self.btnCopyTrack)
        copyButton.grid(row=2, column=self.clm())

        pasteButton = Button(self.top, text="Paste", command=self.btnPasteTrack)
        pasteButton.grid(row=2, column=self.clm())

        duplicateButton = Button(self.top, text="Duplicate", command=self.btnDuplicateTrackSection)
        duplicateButton.grid(row=2, column=self.clm())

        deleteButton = Button(self.top, text="Delete Notes", command=self.delNotes)
        deleteButton.grid(row=2, column=self.clm())

        Label(self.top, text="From").grid(row=2, column=self.clm())

        defaultFrom = StringVar()
        defaultFrom.set('1')  # set the default option
        fromDropDown= OptionMenu(self.top, defaultFrom,1, 4, 9,13,17, 21,25,29)
        fromDropDown.grid(row=2, column=self.clm())

        Label(self.top, text="To").grid(row=2, column=self.clm())

        defaultTo = StringVar()
        defaultTo.set('32')  # set the default option
        toDropDown = OptionMenu(self.top, defaultTo, 4, 8, 12, 16, 20, 24, 28,32)
        toDropDown.grid(row=2, column=self.clm())

        self.clm0()




        b = Button(self.top, text="OK", command=self.ok)
        b.grid(row=3, column=self.clm())

        c = Button(self.top, text="Cancel", command=self.cancel)
        c.grid(row=3, column=self.clm())






    def ok(self):
        self.instrument = int(self.txtInstrument.get())
        self.channel = int(self.txtChannel.get())
        self.velocity = int(self.txtVelocity.get())
        self.top.destroy()

    def cancel(self):
        self.top.destroy()

    def delNotes(self):
        self.parent.remove_beats(self.currRow)

    def btnMuteUnmute(self):
        print ""

    def btnCopyTrack(self):
        print ""

    def btnPasteTrack(self):
        print ""

    def btnDuplicateTrackSection(self):
        print ""

