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





class Piano:


    ##########################################################
    # Description: __init__ is a method that creates         #
    # the window, colors it and calls init_user_interface.   #
    #                                                        #
    # Accepts: self, which contains the window; parent,      #
    # which is a reference to the window.                    #
    ##########################################################
    def __init__(self, parentself,srcBtn,rowNum):

        # This is the initialization of the window along with the
        # coloring of the background.
        #Frame.__init__(self, parent, background='SkyBlue3')

        self.top = Toplevel(parentself.root)
        self.hover = False
        self.top.geometry('800x200')

        self.parentself = parentself
        self.rowNum = rowNum
        if self.rowNum!=None:
            self.hover=True

        # So that the parent reference does not go out of scope.
        self.parent = parentself.root

        self.btn = srcBtn
        self.dict = parentself.dict
        self.mididict = parentself.mididict



        # A call to the init_user_interface method.
        self.init_user_interface()


        #print self.btn

    def label_released(self,other):
        print other.widget.name
        #self.btn.config(text=other.widget.name)
        #self.btn.config(bg='green')

    def button_pressed(self,other):
        note= other.widget.name
        if self.btn!=None:
            self.btn.config(text=note)
            self.dict[note].play()
            self.btn.config(bg='green')
            self.parentself.bass_load(note, 4)
            if not self.hover:
                self.top.destroy()
        else:
            self.parentself.hitKey(note,self.rowNum)


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

        counter = 60
        for key in keys:
            self.dict[key[1]] =  pygame.mixer.Sound('notes/' + key[1] + '.wav')
            self.mididict[key[1]] = counter
            counter = counter + 1

        print self.dict
        # This group of lines creates the record Label.
        # img = PhotoImage(file='pictures/red_button.gif')
        # record_button = Label(self.top, image=img, bd=0)
        # record_button.image = img
        # record_button.place(x=700, y=0)
        # record_button.name = 'red_button'
        # #record_button.bind('<Button-1>', record_on_off)

        # This group of lines creates the play Label.
        # img = PhotoImage(file='pictures/green_button.gif')
        # play_button = Label(self.top, image=img, bd=0)
        # play_button.image = img
        # play_button.place(x=700, y=50)
        # play_button.name = 'green_button'
        # play_button.bind('<Button-1>', play_back)
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


        # These 2 lines bind the '1' and '2' keys on the keyboard
        # to the playback method, which then hooks them up to their
        # respective files. This is mostly for demonstration and
        # experimentation purposes.
        # self.parent.bind('1', play_back)
        # self.parent.bind('2', play_back)

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