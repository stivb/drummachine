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

#the logic now is that this dialog merely sets values inside the
#drum_machine class - the values in its spinboxes are just the relevant variables



class NewSongDialog:



    def __init__(self,parentself):

        self.fileLoc = ""
        self.parent = parentself


    def init_user_interface(self):
        self.top = Toplevel(self.parent.root)
        self.top.geometry('800x200')

        Label(self.top, text='BPM:').grid(row=4, column=0)

        self.bpm_widget = Spinbox(self.top, from_=80, to=160, width=5, textvariable=self.parent.bpmTxt)
        self.bpm_widget.grid(row=4, column=1)

        Label(self.top, text='Units:').grid(row=4, column=2)
        self.units_widget = Spinbox(self.top, from_=1, to=8, width=5, textvariable=self.parent.units)
        self.units_widget.grid(row=4, column=3)
        #
        Label(self.top, text='BPUs:').grid(row=4, column=4)
        self.bpu_widget = Spinbox(self.top, from_=1, to=10, width=5, textvariable=self.parent.bpu)
        self.bpu_widget.grid(row=4, column=5)

        b = Button(self.top, text="OK", command=self.ok)
        b.grid(row=5, column=2)

    def ok(self):
        self.instrument = int(self.txtInstrument.get())
        self.channel = int(self.txtChannel.get())
        self.velocity = int(self.txtVelocity.get())
        self.top.destroy()


    def ok(self):
        return True

