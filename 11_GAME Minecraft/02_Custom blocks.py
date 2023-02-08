# 00 Setup | # 01 Voxels | # 02 Custom

from ursina import * # 00
from ursina.prefabs.first_person_controller import FirstPersonController # 01

app = Ursina() # 00

# 02 Textures = T
T_grass = load_texture('textures/grass_block.png')
T_stone = load_texture('textures/stone_block.png')
T_brick = load_texture('textures/brick_block.png')
T_dirt = load_texture('textures/dirt_block.png')
block_pick = 1

def update():
    global block_pick
    if held_keys['1']: block_pick = 1
    if held_keys['2']: block_pick = 2
    if held_keys['3']: block_pick = 3
    if held_keys['4']: block_pick = 4

class Voxel(Button): # 01
    def __init__(self, position= (0,0,0), texture= T_grass): # 02
        super().__init__(
            parent= scene,
            position= position,
            model= '3d models/block',
            origin_y= 0.5,
            texture= texture, # 02
            # hsv color
            color= color.color(0,0,random.uniform(0.9,1)),
            scale= 0.5 )

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                if block_pick == 1: voxel = Voxel(position= self.position +mouse.normal, texture= T_grass)
                if block_pick == 2: voxel = Voxel(position= self.position +mouse.normal, texture= T_stone)
                if block_pick == 3: voxel = Voxel(position= self.position +mouse.normal, texture= T_brick)
                if block_pick == 4: voxel = Voxel(position= self.position +mouse.normal, texture= T_dirt)

            if key == 'right mouse down':
                destroy(self)                

# 01 Creating voxels 
for z in range(20):
    for x in range(20):
        voxel = Voxel(position= (x,0,z))
player = FirstPersonController()

app.run() # 00