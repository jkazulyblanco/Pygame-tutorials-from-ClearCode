# 00 Grid |

from ursina import *

# 00 Grid classes
class BG(Entity):
    def __init__(self):
        super().__init__(
            parent= camera.ui,
            model= 'quad',
            scale= (0.56,0.86),
            texture= load_texture('graphics/bg.jpg') )

class Item(Draggable):
    def __init__(self):
        super().__init__(
            parent= camera.ui,
            model= 'quad',
            color= color.red,
            scale= (0.1,0.1) )
    
    # def drag(self):
    #     print('drag')

    # get position    
    def drop(self):
        print(f'x: {self.x}')
        print(f'y: {self.y}')

class Grid(Entity):
    def __init__(self):
        super().__init__(
            parent= camera.ui,
            model= 'quad',
            texture= load_texture('graphics/frame.png'),
            texture_scale= (5,8),
            scale= (0.5,0.8) )

app = Ursina()

# 00 Grid objects
bg = BG()
item = Item()
menu_grid = Grid()

app.run()