from gtts import gTTS
import pygame
import os

def say(texto):
    try:
        tts = gTTS(text=texto, lang='es')
        filename = 'temp.mp3'
        tts.save(filename)
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        os.remove(filename)
    except(Exception):
        pass