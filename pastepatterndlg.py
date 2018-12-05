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





class PastePatternDialog:

    def __init__(self,parentself):
        self.originPattern = 0
        self.destinationPattern = 0

        #logic here:
        #tracks to paste contain a dictionary of key=originTrack value=destinationTrack
        #if it is empty
        #just go to new track (the actual navigation movement will be handled elsewhere
        #on a pasteall command, by default, 0:0,1:1,2:2 etc
        #paste all tracks to their corresponding destination track
        #if destination pattern is not empty, require confirmation
        #on a partial paste, just paste selected tracks to corresponding destination track
        #on a complex paste - e.g 0:3,1:1,2:2

        self.tracksToPaste = {}


        self.parent = parentself


    def init_user_interface(self):
        self.top = Toplevel(self.parent.root)
        self.top.geometry('800x200')

        Label(self.top, text='BPM:').grid(row=4, column=0)
        self.bpmTxt = IntVar()
        self.bpmTxt.set(120)
        self.bpu_widget = Spinbox(self.top, from_=80, to=160, width=5, textvariable=self.bpmTxt,
                                  command=self.setBpm)
        self.bpu_widget.grid(row=4, column=1)

        Label(self.top, text='Units:').grid(row=4, column=2)
        self.units = IntVar()
        self.units.set(8)
        self.units_widget = Spinbox(self.top, from_=1, to=8, width=5, textvariable=self.units,
                                    command=self.setUnits)
        self.units_widget.grid(row=4, column=3)
        #
        Label(self.top, text='BPUs:').grid(row=4, column=4)
        self.bpu = IntVar()
        self.bpu.set(4)
        self.bpu_widget = Spinbox(self.top, from_=1, to=10, width=5, textvariable=self.bpu,
                                  command=self.setBpu)
        self.bpu_widget.grid(row=4, column=5)

        b = Button(self.top, text="OK", command=self.ok)
        b.grid(row=5, column=2)

    def ok(self):
        self.instrument = int(self.txtInstrument.get())
        self.channel = int(self.txtChannel.get())
        self.velocity = int(self.txtVelocity.get())
        self.top.destroy()

    def setBpu(self):
        self.bpu=4

    def setUnits(self):
        self.units=8

    def setBpm(self):
        self.bpm = 120

    def ok(self):
        return True