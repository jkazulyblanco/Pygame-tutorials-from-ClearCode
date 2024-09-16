from csv import reader
import pygame
from settings import *
from os import walk

# Import csv file only read
def import_csv_layout(path):
    terrain_map = []
    with open(path) as map: # store all info of csv into map
        level = reader(map, delimiter= ',') # read file csv, separated by ,
        
        for row in level:
            terrain_map.append(list(row))
        return terrain_map
    
def import_cut_graphics(path, tilewidth, tileheight):
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = surface.get_size()[0] // tilewidth
    tile_num_y = surface.get_size()[1] // tileheight

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * tilewidth
            y = row * tileheight
            new_rect = pygame.Rect(x, y, tilewidth, tileheight)
            new_surf = surface.subsurface(new_rect)
            cut_tiles.append(new_surf)
    return cut_tiles

def import_folder(path):
    images_list = []
    for _, __, image_files in walk(path):
        for image in image_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            images_list.append(image_surf)
    return images_list