#!/usr/bin/env python

from midiutil import MIDIFile
import drum_machine



# degrees  = [60, 62, 64, 65, 67, 69, 71, 72]  # MIDI note number
# track    = 0
# channel  = 0
# time     = 0    # In beats
# duration = 1    # In beats
# tempo    = 60   # In BPM
# volume   = 100  # 0-127, as per the MIDI standard
#
# MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
#                       # automatically)
# MyMIDI.addTempo(track, time, tempo)
#
# for i, pitch in enumerate(degrees):
#     MyMIDI.addNote(track, channel, pitch, time + i, duration, volume)
#
# with open("major-scale.mid", "wb") as output_file:
#     MyMIDI.writeFile(output_file)


class midWriter:

    def __init__(self):
        self.track    = 0
        self.channel  = 0
        self.time     = 0    # In beats
        self.duration = 1    # In beats
        self.tempo    = 120   # In BPM
        self.volume   = 100  # 0-127, as per the MIDI standard

    def writeSong(self,ascii_text):
        MyMIDI = MIDIFile(1)
        MyMIDI.addTempo(self.tempo, self.time , self.tempo)
        for lines in ascii_text.split("\n"):
            ct=0
            for note in lines.split(","):
                if note=="":
                    continue
                if (ct<4):
                    channel=10
                else:
                    channel=33
                MyMIDI.addNote(MyMIDI, self.track, channel, note, self.time, 1, 127)
            self.time=self.time+1
        with open("myfilename.mid", "wb") as output_file:
            MyMIDI.writeFile(output_file)
