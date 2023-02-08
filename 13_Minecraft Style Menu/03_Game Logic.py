# 00 Grid | 01 snap to grid | 02 Texturing | 03 Game logic 
# press A to create and drag the mouse 

from ursina import *
from random import choice

# 00 Grid classes
class BG(Entity):
    def __init__(self):
        super().__init__(
            parent= camera.ui,
            model= 'quad',
            scale= (0.56,0.86),
            texture= load_texture('graphics/bg.jpg'),
            position=(0,0,0.01) )

class Item(Draggable): # red quad
     # container parent for create an instace copy
    def __init__(self, container, type, pos): # 02
        super().__init__(
            parent= container,
            model= 'quad',
            color= color.white,
            texture= type, # 02
            # 01 size origin
            scale_x= 1/(container.texture_scale[0]*1.2),
            scale_y= 1/(container.texture_scale[1]*1.2),
            origin= (-0.6,0.6),
            position=(0,0,-0.01),
            x = pos[0] * 1/container.texture_scale[0], # 03
            y = pos[1] * 1/container.texture_scale[1] ) # 03
    
    def drag(self): # 01
        self.xy_pos = (self.x, self.y)

    # get position    
    def drop(self): # 01
        # self.x = 1/5
        # self.y = -1/8
        self.x = int((self.x + self.scale_x/2) *5) /5
        self.y = int((self.y - self.scale_y/2) *8) /8
        self.menu_constraint()
        self.overlap_check()

    def overlap_check(self):
        # 04 check all children inside of grid
        for child in self.parent.children:
            # if overlap with other child == same position
            if child.x == self.x and child.y == self.y:
                # the first selected with mouse works normally
                if child == self: continue
                else: # the second child move to the position of the first
                    child.x = self.xy_pos[0]
                    child.y = self.xy_pos[1]


    def menu_constraint(self): # 01
        # limit of grid
        if self.x < 0 or self.x > 0.95 or self.y > 0 or self.y < -0.95:
            self.x = self.xy_pos[0]
            self.y = self.xy_pos[1]

    def get_cell_pos(self): # 03
        x = int(self.x * self.parent.texture_scale[0])
        y = int(self.y * self.parent.texture_scale[1])
        return Vec2(x,y)

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
        # 02 images
        self.import_textures()
        # 01 add red quad
        self.add_new_item()

    def add_new_item(self):
        # instance copy
        pos = self.find_free_cell()
        # 03
        if pos : Item(self, choice(self.textures), pos)  # 02 select texture item number

    def find_free_cell(self): # 03
        # all posible cells of grid, return all positions
        all_cells = [Vec2(x,y) for y in range(0,-8, -1) for x in range(0,5)]
         # cells that has something
        taken_cells = [child.get_cell_pos() for child in self.children]

        if len(taken_cells) >= len(all_cells):
            return False

        # compare two list to know what cells are free
        for cell in all_cells:
            if cell not in taken_cells:
                return cell
        
        return all_cells

    def import_textures(self): # 02
        grass = load_texture('graphics/grass.png')
        horse = load_texture('graphics/horse.png')
        player = load_texture('graphics/player.png')
        tree = load_texture('graphics/tree.png')
        self.textures = [grass, horse, player, tree]

# 03 Controller
def input(key):
    if key == 'a':
        menu_grid.add_new_item()    

app = Ursina()

# 00 Grid objects
bg = BG()
menu_grid = Grid()

app.run()