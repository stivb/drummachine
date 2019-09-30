#!/usr/bin/env python

from midiutil import MIDIFile
import drum_machine
import re






class midWriter:

    def __init__(self):
        self.numtracks=6
        self.track    = 0
        self.channel  = 0
        self.time     = 0    # In beats
        self.duration = 1    # In beats
        self.tempo    = 120   # In BPM
        self.volume   = 100  # 0-127, as per the MIDI standard

    def writeSong(self,ascii_text):
        while "\n\n" in ascii_text:
            ascii_text = ascii_text.replace("\n\n","\n")
        print "the number of strings is"
        print len(ascii_text.split('\n'))
        print ascii_text

        MyMIDI = MIDIFile(1)
        MyMIDI.addTempo(0, 0, 120)
        MyMIDI.numTracks = self.numtracks
        #for i in range(6):
            #MyMIDI.addTempo(i,0,120)
        beatCt=0
        trackCt=0
        for lines in ascii_text.split("\n"):
            trackCt=0

            print str(len(lines.split(","))) + ":" + lines + ":Track=" + str(trackCt) + ":Time=" + str(self.time)
            for note in lines.split(","):
                if note=="":
                    continue
                if len(lines.split(","))!=6:
                    continue
                if (trackCt<4):
                    channel=9
                else:
                    channel=33
                #print "adding " + str(self.track) + " " + str(channel) + " " + str(note) + " " + str(self.time) + " 1  127"
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