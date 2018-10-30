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
import matplotlib.pyplot as plt








class Song:

    def __init__(self):
        self.cursor = 0
        self.breaks = []
        self.changes = {}
        self.cmap=plt.get_cmap("tab20")
        self.nPatterns  = 1


    def getColForPattern(self,num):
        rgba = self.cmap(num/self.nPatterns)
        return rgba


    def addBreaks(self,brk,times=1):
        for c in range(times):
            self.breaks.append(brk)

    def addBreaksAt(self,brk,at,times=1):
        tmpList = []
        for c in range(times):
            tmpList.append(brk)
        self.breaks[:at]=tmpList


    def makeChangesDictionary(self):
        self.changes[0] = self.breaks[0]
        for i in range(1,len(self.breaks)):
            if self.breaks[i]!=self.breaks[i-1]:
                self.changes[i] = self.breaks[i]


    def toString(self):
        retval = ""
        for bs in self.breaks:
            retval = retval + bs.toString() + "\n"
        return retval;


class Break:
    def __init__(self):
        self.pattern = 0
        self.transpose = 0g
        self.startAt = 0
        self.endAt = 31

    def __eq__(self, other):
        return self.pattern == other.pattern and self.transpose == other.transpose and self.startAt==other.startAt and self.endAt==other.endAt


    def toString(self):
        return "P" + self.pattern + " T" + self.transpose + ":" + self.startAt + "-" + self.endAt

