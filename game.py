#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame import Color
from pygame.locals import *
from sys import exit
from random import randrange

pygame.init()
pygame.font.init()
pygame.mixer.pre_init(44100, 32, 2, 4096)

clock = pygame.time.Clock()

font_name = pygame.font.get_default_font()
game_font = pygame.font.SysFont(font_name, 72)

SCREEN_SIZE = (1024, 768)
screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)

background = pygame.Surface(SCREEN_SIZE)

players = []

actions_file = open('actions.db', 'r')

def create_player():
    player =  {
        'surface': pygame.Surface((50, 50)),
        'position': {'x': randrange(SCREEN_SIZE[0]-50),
                    'y': randrange(SCREEN_SIZE[1]-50)}
    }
    player['surface'].fill(Color(randrange(110, 256),randrange(110, 256),randrange(110, 256)))
    print(player)
    return player

def add_players():
    has_player = True
    while has_player:
        data = actions_file.readline()
        if data:
            if data == 'STARTGAME\n':
                has_player = False
                continue
            players.append(create_player())
add_players()

def draw():
    screen.blit(background, (0, 0))
    for player in players:
        screen.blit(player['surface'], player['position'].values())
    pygame.display.update()

def check_exit():
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()


while True:
    check_exit()
    draw()
    time_passed = clock.tick(30)
