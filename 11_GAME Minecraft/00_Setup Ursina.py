# 00 # setup | # 01 # Entities | # 02 # 3D Entities

from ursina import * # 00

class Test_cube(Entity): # 02
    def __init__(sefl):
        super().__init__(
            model= 'cube',
            color = color.white,
            texture='white_cube',
            rotation= Vec3(45,45,45) )        

class Test_button(Button): # 02
    def __init__(sefl):
        super().__init__(
            parent= scene,
            model= 'cube',
            color = color.blue,
            texture='brick',
            position= (3,0),
            highlight_color= color.cyan,
            pressed_color= color.lime )

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                print('button pressed')


def update():
    if held_keys['a']: 
        test_square.x -= 1 * time.dt # 01


app = Ursina() # 00

# 01 # entities
test_square = Entity(model= 'quad', color= color.red, scale= (1,4), position=(5,2))
sans = Entity(model='quad', texture='textures/sans.png', position= (-5,1))
# 02 #
test_cube = Test_cube()
test_button = Test_button()


app.run() # 00