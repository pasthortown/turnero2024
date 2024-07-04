from gtts import gTTS
import pygame
import os
import time

def say(texto):
    try:
        tts = gTTS(text=texto, lang='es')
        filename = 'temp.mp3'
        tts.save(filename)
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        pygame.mixer.quit()
        os.remove(filename)
    except(Exception):
        pass