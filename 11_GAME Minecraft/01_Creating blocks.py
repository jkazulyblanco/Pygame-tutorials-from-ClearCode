# 00 Setup | # 01 Voxels |

from ursina import * # 00
from ursina.prefabs.first_person_controller import FirstPersonController # 01

class Voxel(Button): # 01
    def __init__(self, position= (0,0,0)):
        super().__init__(
            parent= scene,
            position= position,
            model= 'cube',
            origin_y= 0.5,
            texture= 'white_cube',
            # hsv color
            color= color.color(180,0.3,random.uniform(0.9,1)),
            highlight_color = color.lime )

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                voxel = Voxel(position= self.position + mouse.normal)

            if key == 'right mouse down':
                destroy(self)                

app = Ursina() # 00

# 01 Creating voxels 
for z in range(20):
    for x in range(20):
        voxel = Voxel(position= (x,0,z))
player = FirstPersonController()

app.run() # 00