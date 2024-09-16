import pygame
from os import walk # walk return dirpath, dirnames, filenames
#   _ --> ignore dirpath 
#   __ --> ignore dirnames
# img_file --> filenames

def import_folder(path):
    suface_list = []
    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            suface_list.append(image_surf)
    return suface_list            