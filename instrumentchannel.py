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





class InstrumentChannel:



    def __init__(self,parentself,i,v,c):
        self.instrument = i
        self.velocity = v
        self.channel = c
        self.parent = parentself


    def init_user_interface(self):
        self.top = Toplevel(self.parent.root)
        self.top.geometry('800x200')

        Label(self.top, text="Instrument").pack()
        self.txtInstrument = Entry(self.top)
        self.txtInstrument.insert(END,str(self.instrument))
        self.txtInstrument.pack(padx=5)

        Label(self.top, text="Channel").pack()
        self.txtChannel = Entry(self.top)
        self.txtChannel.insert(END,str(self.channel))
        self.txtChannel.pack(padx=5)

        Label(self.top, text="Velocity").pack()
        self.txtVelocity = Entry(self.top)
        self.txtVelocity.insert(END,str(self.velocity))
        self.txtVelocity.pack(padx=5)

        b = Button(self.top, text="OK", command=self.ok)
        b.pack(pady=5)

    def ok(self):
        self.instrument = int(self.txtInstrument.get())
        self.channel = int(self.txtChannel.get())
        self.velocity = int(self.txtVelocity.get())
        self.top.destroy()

