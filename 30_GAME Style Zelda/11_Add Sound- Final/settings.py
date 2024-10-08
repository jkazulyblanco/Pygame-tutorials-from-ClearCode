# Global Imports
import pygame
from random import choice, randint
from pygame.math import Vector2 as vec2

# game setup
WINDOW = screen_width, screen_height = 1280, 720
TILE = 64

# Weapons
weapon_data = {
    'sword': {'cooldown':100, 'damage':15, 'graphic':'../graphics/weapons/sword/full.png'},
    'lance': {'cooldown':400, 'damage':30, 'graphic':'../graphics/weapons/lance/full.png'},
    'axe':   {'cooldown':300, 'damage':20, 'graphic':'../graphics/weapons/axe/full.png'},
    'rapier':{'cooldown': 50, 'damage': 8, 'graphic':'../graphics/weapons/rapier/full.png'},
    'sai':   {'cooldown': 80, 'damage':10, 'graphic':'../graphics/weapons/sai/full.png'},
}
# Magic
magic_data = {
    'flame': {'strength':5, 'cost':20, 'graphic':'../graphics/particles/flame/fire.png'},
    'heal': {'strength':20, 'cost':10, 'graphic':'../graphics/particles/heal/heal.png'}
}
# Enemy
monster_data = {
    'squid':  {'health':100, 'exp':100, 'damage':20, 'attack_type':'slash',      'attack_sound':'../audio/attack/slash.wav',   'speed':3, 'resistance':3, 'attack_radius':80, 'notice_radius':360},
    'raccoon':{'health':300, 'exp':250, 'damage':40, 'attack_type':'claw',       'attack_sound':'../audio/attack/claw.wav',    'speed':2, 'resistance':3, 'attack_radius':120,'notice_radius':400},
    'spirit': {'health':100, 'exp':110, 'damage': 8, 'attack_type':'thunder',    'attack_sound':'../audio/attack/fireball.wav','speed':4, 'resistance':3, 'attack_radius':60, 'notice_radius':350},
    'bamboo': {'health': 70, 'exp':120, 'damage': 6, 'attack_type':'leaf_attack','attack_sound':'../audio/attack/slash.wav',   'speed':3, 'resistance':3, 'attack_radius':50, 'notice_radius':300}
}


# User Interface
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = '../graphics/font/joystix.ttf'
UI_FONT_SIZE = 18

# General colors
WATER_COLOR = 'deepskyblue4'
UI_BG_COLOR = '#555555'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'
TEXT_COLOR_SELECTED = 'magenta'

# UI colors
HEALTH_COLOR = 'green3'
ENERGY_COLOR = 'darkorange'
UI_BORDER_COLOR_ACTIVE = 'cyan'