import pygame

pygame.mixer.init()

def play_correct():
    pygame.mixer.Sound("assets/sounds/correct.wav").play()

def play_wrong():
    pygame.mixer.Sound("assets/sounds/wrong.mp3").play()
