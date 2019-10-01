#!/usr/bin/env python

from midiutil import MIDIFile
import drum_machine
import re






class midWriter:

    def __init__(self):
        self.numtracks = 7
        self.track = 0
        self.channel = 0
        self.time = 0  # In beats
        self.duration = 1  # In beats
        self.tempo = 120  # In BPM
        self.volume = 100


    def reset(self):
        self.numtracks = 7
        self.track = 0
        self.channel = 0
        self.time = 0  # In beats
        self.duration = 1  # In beats
        self.tempo = 120  # In BPM
        self.volume = 100

    def getCountIn(self):
        retval=""
        for i in range(4):
            retval=retval+"36,36,36,36,48,48\n,,,,,\n,,,,,\n,,,,,\n"
        return retval

    def writeSong(self,ascii_text):
        self.reset()
        MyMIDI = MIDIFile(16)
        MyMIDI.addTempo(0, 0, 120)
        MyMIDI.addProgramChange(4, 4, 0, 37)
        MyMIDI.addProgramChange(5, 5, 0, 38)

        ascii_text=self.getCountIn() + ascii_text
        trackCt=0
        for lines in ascii_text.split("\n"):
            trackCt=0

            print str(len(lines.split(","))) + ":" + lines + ":Track=" + str(trackCt) + ":Time=" + str(self.time)
            for note in lines.split(","):
                if note!="":
                    if (trackCt<4):
                        channel=9
                    else:
                        channel=trackCt
                    print "adding " + str(trackCt) + " " + str(channel) + " " + str(note) + " " + str(self.time) + " 1  127"
                    MyMIDI.addNote(trackCt, channel, int(note)-1, self.time, 0.5, 127)
                trackCt=trackCt+1

            if len(lines.split(","))==6:
                self.time=self.time+0.25

        with open("myfilename.mid", "wb") as output_file:
            MyMIDI.writeFile(output_file)

    def writeScale(self):
        degrees  = [60, 62, 64, 65, 67, 69, 71, 72]  # MIDI note number
        track    = 0
        channel  = 0
        time     = 0    # In beats
        duration = 1    # In beats
        tempo    = 60   # In BPM
        volume   = 100  # 0-127, as per the MIDI standard

        MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
                              # automatically)
        MyMIDI.addTempo(track, time, tempo)

        for i, pitch in enumerate(degrees):
            MyMIDI.addNote(track, channel, pitch, time + i, duration, volume)

        with open("major-scale.mid", "wb") as output_file:
            MyMIDI.writeFile(output_file)