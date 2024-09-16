# 00 Grid | # 01 snap to grid

from ursina import *

# 00 Grid classes
class BG(Entity):
    def __init__(self):
        super().__init__(
            parent= camera.ui,
            model= 'quad',
            scale= (0.56,0.86),
            texture= load_texture('graphics/bg.jpg') )

class Item(Draggable): # red quad
     # container parent for create an instace copy
    def __init__(self, container):
        super().__init__(
            parent= container,
            model= 'quad',
            color= color.red,
            # 01 size origin
            scale_x= 1/(container.texture_scale[0]*1.2),
            scale_y= 1/(container.texture_scale[1]*1.2),
            origin= (-0.6,0.6) )
    
    def drag(self): # 01
        self.xy_pos = (self.x, self.y)

    # get position    
    def drop(self): # 01
        # self.x = 1/5
        # self.y = -1/8
        self.x = int((self.x + self.scale_x/2) *5) /5
        self.y = int((self.y - self.scale_y/2) *8) /8
        self.menu_constraint()

    def menu_constraint(self): # 01
        # limit of grid
        if self.x < 0 or self.x > 0.95 or self.y > 0 or self.y < -0.95:
            self.x = self.xy_pos[0]
            self.y = self.xy_pos[1]

class Grid(Entity):
    def __init__(self):
        super().__init__(
            parent= camera.ui,
            model= 'quad',
            texture= load_texture('graphics/frame.png'),
            texture_scale= (5,8),
            scale= (0.5,0.8),
            # 01 changin the origin to top left
            origin= (-0.5,0.5),
            position= (-0.25,0.4) ) # half of texture_scale
        
        # 01 add red quad
        self.add_new_item()

    def add_new_item(self):
        Item(self) # instance copy

app = Ursina()

# 00 Grid objects
bg = BG()
menu_grid = Grid()

app.run()