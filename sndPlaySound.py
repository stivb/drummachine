import os
import pygame
from Tkinter import *
import tkFileDialog
import tkMessageBox

def load_sound(sound_filename, directory):
    """load the sound file from the given directory"""
    fullname = os.path.join(directory, sound_filename)
    tkMessageBox.showinfo("audio file", fullname)
    sound = pygame.mixer.Sound(fullname)
    return sound

pygame.init()

# some color tuples (r,g,b)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
screen = pygame.display.set_mode([600, 400])
pygame.display.set_caption("Simple Play Wave Files")

directory = "loops"
chimes = load_sound("cowbell.wav", directory)
chord = load_sound("maracas.wav", directory)
notify = pygame.mixer.Sound("loops\cowbell.wav")



# optional color change
screen.fill(red)
pygame.display.flip()
chimes.play()
# milliseconds wait for each sound to finish
pygame.time.wait(2000)
screen.fill(green)
pygame.display.flip()
chord.play()
pygame.time.wait(2000)
screen.fill(blue)
pygame.display.flip()
notify.play()
# event loop and exit conditions
# escape key or display window x click
while True:
    for event in pygame.event.get():
        if (event.type == pygame.QUIT or 
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            raise SystemExit
