#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame import Color
from pygame.locals import *
from sys import exit

pygame.init()
pygame.font.init()
pygame.mixer.pre_init(44100, 32, 2, 4096)

clock = pygame.time.Clock()

font_name = pygame.font.get_default_font()
game_font = pygame.font.SysFont(font_name, 72)

screen = pygame.display.set_mode((1280, 1024), 0, 32)

background = pygame.Surface((1280, 1024))

players = []

actions_file = open('actions.db', 'r')

def create_player():
    return {
        'surface': pygame.Surface((50, 50)).fill(Color(randrange(255), randrange(255), randrange(255))),
        'position': {'x': randrange(1229),
                    'y': randrange(973)}
    }

def add_players():
    has_player = True
    while has_player:
        data = actions_file.readline()
        if data:
            if data == 'STARTGAME':
                has_player = false
                continue
            players.append(create_player())

add_players()

def draw():
    screen.blit(background, (0, 0))
    for player in players:
        screen.blit(player['surface'], player['position'].values())
    pygame.display.update()
    
while True:
    time_passed = clock.tick(30)
