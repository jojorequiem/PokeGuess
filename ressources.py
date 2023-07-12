import pygame
pygame.mixer.init()

# Game images
game_icon = pygame.image.load('images/icon.png')
main_background = pygame.image.load('images/sky_background.jpg')
battle_background = pygame.image.load('images/battlescreen.png')

# Game sounds/musics
start_song = pygame.mixer.Sound('music/start_song.mp3')
start_song.set_volume(0.2)
click_sound_effect = pygame.mixer.Sound('music/click_sound.mp3')
click_sound_effect.set_volume(0.5)
battle_song = pygame.mixer.Sound('music/battle_song.mp3')
battle_song.set_volume(0.5)
victory_sound_effect = pygame.mixer.Sound('music/victory_sound.mp3')
defeat_sound_effect = pygame.mixer.Sound('music/defeat_sound.mp3')
