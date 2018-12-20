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
import pyparsing as pp

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


    def getSequenceArray(self,inputString):
        testPattern = "{0 +0 1-32}*4 {0 +5 1-32}*2 {0}*2 {0 +7 1-32} {0 +5 1-32} {0 +0 1-32} {0 +0 1-16} {0 +7 17-32}"
        if inputString=="":
            inputString = testPattern
        number = pp.Word(pp.nums, max=2)
        plusOrMinus = pp.Word("+-/", max=1)
        transposition = pp.Optional(pp.Combine(plusOrMinus + number))
        lpar = pp.Literal('{').suppress()
        rpar = pp.Literal('}').suppress()
        startend = pp.Optional(pp.Combine(number + "-" + number))
        whitespace = pp.ZeroOrMore(" ")
        space = pp.Optional(pp.OneOrMore(" "))
        pattern = pp.Combine(lpar + number + space + transposition + space + startend + rpar)
        repeatCount = pp.Combine("*" + number)
        patterns = pp.OneOrMore(pattern | repeatCount)

        shorthand = patterns.parseString(inputString)
        longhand = []
        for i in range(len(shorthand)):
            s = shorthand[i]
            print "S is :",s
            if s[0] == '*':
                repeat = int(s[1:]) - 1
                for j in range(repeat):
                    longhand.append(shorthand[i - 1])
            else:
                longhand.append(shorthand[i])

        listOfBreaks = []
        for i in range(len(longhand)):
            b = Break()
            b.setBreak(longhand[i])
            listOfBreaks.append(b)
        print listOfBreaks
        return listOfBreaks

class Break:
    def __init__(self):
        self.pattern = 0
        self.transpose = 0
        self.startAt = 1
        self.stopAt = 32

    def setBreak(self,inputString):
        items = filter(None, inputString.split(' '))
        self.pattern = int(items[0])
        if len(items)>=2:
            self.transpose = int(items[1])
        if len(items)==3:
            startend = items[2]
            self.startAt = int(startend.split('-')[0])
            self.stopAt = int(startend.split('-')[1])


    def __eq__(self, other):
        return self.pattern == other.pattern and self.transpose == other.transpose and self.startAt == other.startAt and self.stopAt == other.endAt

    def toString(self):
        return "{" + str(self.pattern) + " " + str(self.transpose) + " " + str(self.startAt) + "-" + str(self.stopAt) + "}"

    def __repr__(self):
        return self.toString()

