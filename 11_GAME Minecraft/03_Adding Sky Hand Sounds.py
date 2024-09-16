# 00 Setup | # 01 Voxels | # 02 Custom | # 03 Addings

from ursina import * # 00
from ursina.prefabs.first_person_controller import FirstPersonController # 01

app = Ursina() # 00

# 02 Textures = T
T_grass = load_texture('textures/grass_block.png')
T_stone = load_texture('textures/stone_block.png')
T_brick = load_texture('textures/brick_block.png')
T_dirt = load_texture('textures/dirt_block.png')
# 03 
T_sky = load_texture('textures/skydome.jpg')
T_arm = load_texture('textures/arm_texture.png')
punch_sound = Audio('punch_sound', loop= False, autoplay= False)
block_pick = 1

# off screen elements
# window.fps_counter.enable = False
# window.exit_button.visible = False

def update():
    global block_pick
    # 03 Hand movement
    if held_keys['left mouse'] or held_keys['right mouse']:
        hand.active()
    else:
        hand.passive()

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
                punch_sound.play()
                if block_pick == 1: voxel = Voxel(position= self.position +mouse.normal, texture= T_grass)
                if block_pick == 2: voxel = Voxel(position= self.position +mouse.normal, texture= T_stone)
                if block_pick == 3: voxel = Voxel(position= self.position +mouse.normal, texture= T_brick)
                if block_pick == 4: voxel = Voxel(position= self.position +mouse.normal, texture= T_dirt)

            if key == 'right mouse down':
                punch_sound.play()
                destroy(self)                

# 03 Sky, Hand, Sound
class Sky(Entity): 
    def __init__(self):
        super().__init__(
            parent= scene,
            model= 'sphere',
            texture= T_sky,
            double_sided= True,
            scale= 150 )

class Hand(Entity):
    def __init__(self):
        super().__init__(
            parent= camera.ui,
            model= '3d models/arm',
            texture= T_arm,
            scale = 0.2,
            rotation= Vec3(150,-10,0),
            position= Vec2(0.4,-0.6) )

    def active(self):
        self.position = Vec2(0.35, -0.65)

    def passive(self):
        self.position = Vec2(0.4, -0.6)

# 01 Creating voxels floor
for z in range(20):
    for x in range(20):
        voxel = Voxel(position= (x,0,z))

player = FirstPersonController() # 01
# 03
sky = Sky() 
hand = Hand()

app.run() # 00