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

SCREEN_SIZE = (800, 600)
screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)

background = pygame.Surface(SCREEN_SIZE)

players = {}

actions_file = open('actions.db', 'r')

game_started = False

bullets = []


def create_player(name):
    player = {
        'name': name,
        'action': [],
        'surface': pygame.Surface((50, 50)),
        'position': {'x': randrange(SCREEN_SIZE[0]-50),
                    'y': randrange(SCREEN_SIZE[1]-50)},
        'motion': {'direction': '',
                    'distance': 0}
    }
    player['surface'].fill(Color(randrange(110, 256),randrange(110, 256),randrange(110, 256)))
    print(player)
    return player


def add_players():
    global game_started
    has_player = True
    while has_player:
        data = actions_file.readline().strip()
        if data:
            print(data)
            if data == 'STARTGAME':
                has_player = False
                game_started = True
                continue
            print data
            action, ip, name = data.split(':')
            players[ip] = create_player(name)
        else:
            return


def create_bullet(ip, position, direction):
    bullet = {
        'origin': ip,
        'surface': pygame.Surface((10, 10)),
        'position': dict(position),
    }
    bullet['surface'].fill(Color(255, 0, 0))
    if direction == 0:
        bullet['speed'] = (0, -10)
    elif direction == 1:
        bullet['speed'] = (10, 0)
    elif direction == 2:
        bullet['speed'] = (0, 10)
    elif direction == 3:
        bullet['speed'] = (-10, 0)

    bullets.append(bullet)


def draw():
    screen.blit(background, (0, 0))
    for player in players.values():
        screen.blit(player['surface'], player['position'].values())
    for bullet in bullets:
        screen.blit(bullet['surface'], bullet['position'].values())
    pygame.display.update()


def check_exit():
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()


def process_action(data):
    action = data.split(':')
    players[action[1]]['action'].append('{}({}, {})'.format(action.pop(0), '"{}"'.format(action.pop(0)), ','.join(action)))


def goto(ip, direction, distance):
    players[ip]['motion']['distance'] = distance
    players[ip]['motion']['direction'] = direction


def shoot(ip, direction):
    create_bullet(ip, players[ip]['position'], direction)


def get_action():
    data = actions_file.readline().strip()
    while data:
        process_action(data)
        data = actions_file.readline()


def move_player(player):
    direction = player['motion']['direction']
    if direction == 0:
        player['position']['y'] -= 10
    elif direction == 1:
        player['position']['x'] += 10
    elif direction == 2:
        player['position']['y'] += 10
    elif direction == 3:
        player['position']['x'] -= 10

    player['motion']['distance'] -= 10


def execute_actions():
    for player in players.values():
        if player['motion']['distance']:
            move_player(player)
        else:
            try:
                action = player['action'].pop(0)
                eval(action)
            except:
                pass


def move_bullets():
    for bullet in bullets:
        bullet['position']['x'] += bullet['speed'][0]
        bullet['position']['y'] += bullet['speed'][1]


def get_rect(obj):
    return Rect(obj['position']['x'],
                obj['position']['y'],
                obj['surface'].get_width(),
                obj['surface'].get_height())


def check_player_hit():
    bullet_rects = [get_rect(b) for b in bullets]
    for ip, player in players.items():
        r = get_rect(player)
        collided = r.collidelist(bullet_rects)
        if collided >= 0 and bullets[collided]['origin'] != ip:
            del(players[ip])
            bullets.pop(collided)


def clear_lost_bullets():
    for bullet in bullets[:]:
        if bullet['position']['x'] < 0 or bullet['position']['x'] > SCREEN_SIZE[0] or bullet['position']['y'] < 0 or bullet['position']['y'] > SCREEN_SIZE[1]:
            bullets.remove(bullet)


while True:

    check_exit()

    if not game_started:
        add_players()
    else:
        get_action()

        execute_actions()
        move_bullets()
        check_player_hit()
    draw()
    time_passed = clock.tick(30)
