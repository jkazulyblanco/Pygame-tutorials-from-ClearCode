import pygame, sys
from pytmx.util_pygame import load_pygame

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1280,720), vsync=1)

# Surfaces ==============================================
tmx_data = load_pygame('../data/tmx/basic.tmx')
# ▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄
'''
print(dir(tmx_data)) # see all the data to access 

# get Layers of map -------------------------------------
print(tmx_data.layers) # all layers
for layer in tmx_data.visible_layers: print(layer) # show only visible layers
print(tmx_data.layernames) # dict of all layer names
print(tmx_data.get_layer_by_name('Floor'))

# get tiles ---------------------------------------------
layer = tmx_data.get_layer_by_name('Floor')
# print(dir(layer))

for tile in layer.tiles(): print(tile) # get = x, y, suruface
for x, y, surf in layer.tiles(): # get all the information
    print(x*128,   y*128) # get positions = x, y

print(layer.data) # csv data
print(layer.name)
print(layer.id)
'''
# get Objects -------------------------------------------
# for obj in tmx_data.objectgroups: print(obj) # get object layers
# object_layer = tmx_data.get_layer_by_name('Objects')
# print(dir(object_layer))
# for obj in object_layer: # get all objects of the layer
    # print(obj.x) 
    # print(obj.y) 
    # print(obj.image) 

object_layer = tmx_data.get_layer_by_name('Objects')
for obj in object_layer:  # get all objects of the layer
    # get shape objects
    if obj.name == 'Rectangle':
        print(obj.x)
        print(obj.y)
    #     print(obj.width)
    #     print(obj.height)
    #     print(obj.as_points) # returns bounding box
    #     print(obj.points) # returns current points
    

# Game Loop =============================================
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # Draw - Update =====================================
    screen.fill('black')

    pygame.display.update()
    clock.tick(60)