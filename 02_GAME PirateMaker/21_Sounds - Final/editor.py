import pygame, sys
from pygame.math import Vector2 as vector
from pygame.mouse import get_pressed as mouse_buttons
from pygame.mouse import get_pos as mouse_pos
from pygame.image import load

from settings import *
from support import *

from menu import Menu
from timer import Timer

from random import choice, randint

#█████████████████████████████████████████████████████████
class Editor:
    def __init__(self, land_tiles, switch):
        # main setup
        self.display_surface = pygame.display.get_surface()
        self.canvas_data = {}
        self.switch = switch

        # Imports
        self.land_tiles = land_tiles
        self.imports()

        # Clouds
        self.current_clouds = []
        self.cloud_surf = import_folder('../graphics/clouds')
        self.cloud_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.cloud_timer, 2000)
        self.startup_clouds()

        # Navigation
        self.origin = vector()
        self.pan_active = False
        self.pan_offset = vector()

        # Support Lines - screen layer for lines
        self.support_line_surf = pygame.Surface((WINDOW_WIDTH,WINDOW_HEIGHT))
        self.support_line_surf.set_colorkey('green')
        self.support_line_surf.set_alpha(30)

        # Selection - menu
        self.selection_index = 2
        self.last_selected_cell = None

        # Menu
        self.menu = Menu()

        # Objects
        self.canvas_objects = pygame.sprite.Group()
        self.foreground = pygame.sprite.Group()
        self.background = pygame.sprite.Group()
        self.object_drag_active = False
        self.object_timer = Timer(400)

        # Player
        CanvasObject(
            pos= (200, WINDOW_HEIGHT /2),
            frames= self.animations[0]['frames'],
            tile_id= 0,
            origin= self.origin,
            group= [self.canvas_objects, self.foreground])

        # Sky
        self.sky_handle = CanvasObject(
            pos= (WINDOW_WIDTH /2, WINDOW_HEIGHT /2),
            frames= [self.sky_handle_surf],
            tile_id= 1,
            origin= self.origin,
            group= [self.canvas_objects, self.background] )

        # Music
        self.editor_music = pygame.mixer.Sound('../audio/Explorer.ogg')
        self.editor_music.set_volume(0.4)
        self.editor_music.play(loops= -1)

    # SUPPORT ___________________________________
    def get_current_cell(self, obj= None):
        # get pixel position from origin point
        distance_to_origin = vector(mouse_pos()) - self.origin if not obj else vector(obj.distance_to_origin) - self.origin
        # convert pixel position in a cell- divide by tile size 64
        if distance_to_origin.x > 0:
            col = int(distance_to_origin.x / TILE_SIZE)
        else:
            col = int(distance_to_origin.x / TILE_SIZE) -1
        if distance_to_origin.y > 0:
            row = int(distance_to_origin.y / TILE_SIZE)
        else:
            row = int(distance_to_origin.y / TILE_SIZE) -1
        return col, row

    def check_neighbors(self, cell_pos):
        # create a local cluster
        cluster_size = 3 # num of tiles by x and y
        local_cluster = [
            (cell_pos[0] + col - int(cluster_size /2), cell_pos[1] + row - int(cluster_size /2))
            for col in range(cluster_size)
            for row in range(cluster_size)]
        # print(local_cluster)
        
        #  check neighbors
        for cell in local_cluster:
            if cell in self.canvas_data:
                # reset values to default for every change
                self.canvas_data[cell].terrain_neighbors = []
                self.canvas_data[cell].water_on_top = False
                # neighbors cell
                for name, side in NEIGHBOR_DIRECTIONS.items():
                    neighbor_cell = (cell[0] + side[0], cell[1] + side[1])

                    # Water Top Neighbor, water in current tile, and another water tile on top neighbor = A
                    if neighbor_cell in self.canvas_data:
                        if self.canvas_data[neighbor_cell].has_water and self.canvas_data[cell].has_water and name == 'A':
                            self.canvas_data[cell].water_on_top = True
                    
                    # Terrain Neighbors
                        if self.canvas_data[neighbor_cell].has_terrain:
                            self.canvas_data[cell].terrain_neighbors.append(name)

    def imports(self):
        self.water_bottom = load('../graphics/terrain/water/water_bottom.png').convert_alpha()
        self.sky_handle_surf = load('../graphics/cursors/handle.png').convert_alpha()

        # Animations
        self.animations = {}
        for key, value in EDITOR_DATA.items():
            # if value of graphics exist
            if value['graphics']:
                graphics = import_folder(value['graphics'])
                self.animations[key] = {
                    'frame index': 0,
                    'frames': graphics,
                    'length': len(graphics)
                }

        # Preview
        self.preview_surfs = {key: load(value['preview']) for key, value in EDITOR_DATA.items() if value['preview']}

    def animation_update(self, dt):
        for value in self.animations.values():
            value['frame index'] += ANIMATION_SPEED * dt
            if value['frame index'] >= value['length']:
                value['frame index'] = 0       

    def mouse_on_object(self):
        for sprite in self.canvas_objects:
            if sprite.rect.collidepoint(mouse_pos()):
                return sprite

    def create_grid(self):
        # Add objects to the tiles
        for tile in self.canvas_data.values():
            tile.objects = []

        for obj in self.canvas_objects:
            current_cell = self.get_current_cell(obj)
            offset = vector(obj.distance_to_origin) - (vector(current_cell) * TILE_SIZE)
            # tile exists already
            if current_cell in self.canvas_data:
                self.canvas_data[current_cell].add_id(obj.tile_id, offset)
            # no tile exists yet
            else:
                self.canvas_data[current_cell] = CanvasTile(obj.tile_id, offset)


        # Create an empty grid
        layers = {
            'water': {},
            'bg palms': {},
            'terrain': {},
            'enemies': {},
            'coins': {},
            'fg objects': {},
        }

        # Create the grid
        left = sorted(self.canvas_data.keys(), key = lambda tile: tile[0])[0][0]
        top = sorted(self.canvas_data.keys(), key = lambda tile: tile[1])[0][1]
        
        # Fill the Grid
        for tile_pos, tile in self.canvas_data.items():
            row_adjusted = tile_pos[1] - top
            col_adjusted = tile_pos[0] - left
            x = col_adjusted * TILE_SIZE
            y = row_adjusted * TILE_SIZE

            if tile.has_water:
                layers['water'][(x, y)] = tile.get_water()
            if tile.has_terrain:
                layers['terrain'][(x, y)] = tile.get_terrain() if tile.get_terrain() in self.land_tiles else 'X'
            if tile.coin:
                layers['coins'][(x + TILE_SIZE //2, y + TILE_SIZE //2)] = tile.coin
            if tile.enemy:
                layers['enemies'][(x, y)] = tile.enemy
            if tile.objects: # (obj, offset)
                for obj, offset in tile.objects:
                    # bg palm
                    if obj in [key for key, value in EDITOR_DATA.items() if value['style'] == 'palm_bg']:
                        layers['bg palms'][(int(x + offset.x), int(y + offset.y))] = obj
                    # fg objects
                    else: 
                        layers['fg objects'][(int(x + offset.x), int(y + offset.y))] = obj
        return layers

    # INPUT ­­­▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀
    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.switch(self.create_grid())
                self.editor_music.stop()
            
            self.pan_input(event)
            self.selection_hotkeys(event)
            self.menu_click(event)
            
            self.object_drag(event)
            
            self.canvas_add()
            self.canvas_remove()

            self.create_clouds(event)

    def pan_input(self, event):
        # middle mouse button pressed / released
        if event.type == pygame.MOUSEBUTTONDOWN and mouse_buttons()[1]: 
            self.pan_active = True
            self.pan_offset = vector(mouse_pos()) - self.origin

        if not mouse_buttons()[1]:
            self.pan_active = False
        
        # mouse wheel
        if event.type == pygame.MOUSEWHEEL:
            if pygame.key.get_pressed()[pygame.K_LCTRL]:
                self.origin.y -= event.y * 50
            else:
                self.origin.x -= event.y * 50
            for sprite in self.canvas_objects:
                sprite.pan_pos(self.origin) 

        # panning update
        if self.pan_active:
            self.origin = vector(mouse_pos()) - self.pan_offset

            for sprite in self.canvas_objects:
                sprite.pan_pos(self.origin)   

    def selection_hotkeys(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.selection_index += 1
            if event.key == pygame.K_LEFT:
                self.selection_index -= 1
        # clamp from 2 to 18
        self.selection_index = max(2,min(self.selection_index, 18))

    def menu_click(self, event):
        # check if mouse button is pressing on the menu state
        if event.type == pygame.MOUSEBUTTONDOWN and self.menu.rect.collidepoint(mouse_pos()):
            new_index = self.menu.click(mouse_pos(), mouse_buttons())
            self.selection_index = new_index if new_index else self.selection_index

    def canvas_add(self):
        # if the left click is on the menu or canvas
        if mouse_buttons()[0] and not self.menu.rect.collidepoint(mouse_pos()) and not self.object_drag_active:
            current_cell = self.get_current_cell()
            # Put Tile
            if EDITOR_DATA[self.selection_index]['type'] == 'tile':
                if current_cell != self.last_selected_cell:
                    if current_cell in self.canvas_data:
                        self.canvas_data[current_cell].add_id(self.selection_index)
                    else:
                        self.canvas_data[current_cell] = CanvasTile(self.selection_index)

                    self.check_neighbors(current_cell)
                    self.last_selected_cell = current_cell
            else: # Put Object
                if not self.object_timer.active:
                    groups = [self.canvas_objects, self.background] if EDITOR_DATA[self.selection_index]['style'] == 'palm_bg' else [self.canvas_objects, self.foreground]
                    CanvasObject(
                        pos= mouse_pos(),
                        frames= self.animations[self.selection_index]['frames'],
                        tile_id= self.selection_index,
                        origin= self.origin,
                        group= groups )
                    self.object_timer.activate()

    def canvas_remove(self):
        if mouse_buttons()[2] and not self.menu.rect.collidepoint(mouse_pos()):
            # Delete Objects
            selected_object = self.mouse_on_object()
            if selected_object:
                if EDITOR_DATA[selected_object.tile_id]['style'] not in ('player', 'sky'):
                    selected_object.kill()

            # Delete Tiles
            if self.canvas_data:
                current_cell = self.get_current_cell()
                if current_cell in self.canvas_data:
                    self.canvas_data[current_cell].remove_id(self.selection_index)

                    if self.canvas_data[current_cell].is_empty:
                        del self.canvas_data[current_cell]
                    self.check_neighbors(current_cell)

    def object_drag(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and mouse_buttons()[0]:
            for sprite in self.canvas_objects:
                if sprite.rect.collidepoint(event.pos):
                    sprite.start_drag()
                    self.object_drag_active = True

        if event.type == pygame.MOUSEBUTTONUP and self.object_drag_active:
            for sprite in self.canvas_objects:
                if sprite.selected:
                    sprite.drag_end(self.origin)
                    self.object_drag_active = False

    # DRAWING ­▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄
    def draw_tile_lines(self):
        cols = WINDOW_WIDTH  // TILE_SIZE
        rows = WINDOW_HEIGHT // TILE_SIZE

        

        origin_offset = vector(
            x = self.origin.x - int(self.origin.x / TILE_SIZE) * TILE_SIZE,
            y = self.origin.y - int(self.origin.y / TILE_SIZE) * TILE_SIZE)
        
        self.support_line_surf.fill('green')

        for col in range(cols +1):
            x = origin_offset.x + col * TILE_SIZE
            pygame.draw.line(self.support_line_surf, LINE_COLOR, (x, 0), (x, WINDOW_HEIGHT))

        for row in range(rows +1):
            y = origin_offset.y + row * TILE_SIZE
            pygame.draw.line(self.support_line_surf, LINE_COLOR, (0, y), (WINDOW_WIDTH, y))
        
        self.display_surface.blit(self.support_line_surf,(0,0))

    def draw_level(self):
        self.background.draw(self.display_surface)
        for cell_pos, tile in self.canvas_data.items():
            pos = self.origin + vector(cell_pos) * TILE_SIZE
            
            # Water
            if tile.has_water:
                if tile.water_on_top:
                    self.display_surface.blit(self.water_bottom, pos)
                else:
                    frames = self.animations[3]['frames'] # water animation frames
                    index = int(self.animations[3]['frame index'])
                    surf = frames[index]
                    self.display_surface.blit(surf, pos)

            # Terrain
            if tile.has_terrain:    
                terrain_string = ''.join(tile.terrain_neighbors)
                terrain_style = terrain_string if terrain_string in self.land_tiles else 'X'
                self.display_surface.blit(self.land_tiles[terrain_style], pos)

            # Coins
            if tile.coin:
                frames = self.animations[tile.coin]['frames']
                index = int(self.animations[tile.coin]['frame index'])    
                surf = frames[index]
                # fix center tile when only put one coin
                rect = surf.get_rect(center= (pos[0] + TILE_SIZE // 2, pos[1] + TILE_SIZE // 2))
                self.display_surface.blit(surf, rect)

            # Enemies
            if tile.enemy:
                frames = self.animations[tile.enemy]['frames']
                index = int(self.animations[tile.enemy]['frame index'])    
                surf = frames[index]
                # put on floor
                rect = surf.get_rect(midbottom= (pos[0] + TILE_SIZE // 2, pos[1] + TILE_SIZE))
                self.display_surface.blit(surf, rect)
        self.foreground.draw(self.display_surface)

    def preview(self):
        selected_object = self.mouse_on_object()
        
        if not self.menu.rect.collidepoint(mouse_pos()):
            if selected_object:
                # Draws corner lines around objects when hovered over
                rect = selected_object.rect.inflate(10,10)
                color = 'black'
                width = 3
                size = 15
                # Corner lines topleft, topright, bottomleft, bottomright
                pygame.draw.lines(self.display_surface, color, False, ((rect.left, rect.top + size),(rect.topleft),(rect.left + size, rect.top)), width)
                pygame.draw.lines(self.display_surface, color, False, ((rect.right, rect.top + size),(rect.topright),(rect.right - size, rect.top)), width)
                pygame.draw.lines(self.display_surface, color, False, ((rect.left, rect.bottom - size),(rect.bottomleft),(rect.left + size, rect.bottom)), width)
                pygame.draw.lines(self.display_surface, color, False, ((rect.right, rect.bottom - size),(rect.bottomright),(rect.right - size, rect.bottom)), width)
            else:
                # Preview of the tile / object 
                type_dict = {key: value['type'] for key, value in EDITOR_DATA.items()}
                surf = self.preview_surfs[self.selection_index].copy()
                surf.set_alpha(200)
                
                # tile
                if type_dict[self.selection_index] == 'tile':
                    current_cell = self.get_current_cell()
                    rect = surf.get_rect(topleft= self.origin + vector(current_cell) * TILE_SIZE)
                # Object
                else:
                    rect = surf.get_rect(center= mouse_pos())
                self.display_surface.blit(surf, rect)

    def display_sky(self, dt):
        self.display_surface.fill(SKY_COLOR)
        y = self.sky_handle.rect.centery

        # Horizontal Lines
        if y > 0:
            horizon_rec1 = pygame.Rect(0, y-10, WINDOW_WIDTH, 10)
            horizon_rec2 = pygame.Rect(0, y-16, WINDOW_WIDTH, 4)
            horizon_rec3 = pygame.Rect(0, y-20, WINDOW_WIDTH, 2)
            pygame.draw.rect(self.display_surface, HORIZON_TOP_COLOR, horizon_rec1)
            pygame.draw.rect(self.display_surface, HORIZON_TOP_COLOR, horizon_rec2)
            pygame.draw.rect(self.display_surface, HORIZON_TOP_COLOR, horizon_rec3)
            self.display_clouds(dt, y)

        # Draw Sea
        # if horizon is on the screen:
        if 0 < y < WINDOW_HEIGHT:
            sea_rect = pygame.Rect(0,y, WINDOW_WIDTH, WINDOW_HEIGHT)
            pygame.draw.rect(self.display_surface, SEA_COLOR, sea_rect)
            pygame.draw.line(self.display_surface, HORIZON_COLOR, (0,y), (WINDOW_WIDTH,y), 3)
        if y < 0:
            self.display_surface.fill(SEA_COLOR)
        
    def display_clouds(self, dt, horizon_y):
        for cloud in self.current_clouds: # [{surf, pos, speed}]
            cloud['pos'][0] -= cloud['speed'] * dt
            x = cloud['pos'][0]
            y = horizon_y - cloud['pos'][1]
            self.display_surface.blit(cloud['surf'],(x,y))

    def create_clouds(self, event):
        if event.type == self.cloud_timer:
            surf = choice(self.cloud_surf)
            surf = pygame.transform.scale2x(surf) if randint(0,4) < 2 else surf

            pos = [WINDOW_WIDTH + randint(50,100), randint(0, WINDOW_HEIGHT)]
            self.current_clouds.append({'surf': surf, 'pos': pos, 'speed': randint(20,50)})

            # Remove Clouds
            self.current_clouds = [cloud for cloud in self.current_clouds if cloud['pos'][0] > -400]

    def startup_clouds(self):
        for i in range(20):
             surf = pygame.transform.scale2x(choice(self.cloud_surf)) if randint(0,4) < 2 else choice(self.cloud_surf)
             pos = [randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)]
             self.current_clouds.append({'surf': surf, 'pos': pos, 'speed': randint(20,50)})

    # UPDATE ­▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀
    def run(self, dt):
        self.event_loop()

        # Updating
        self.animation_update(dt)
        self.canvas_objects.update(dt)
        self.object_timer.update()

        # Drawing
        self.display_surface.fill('gray')
        self.display_sky(dt)
        self.draw_level()
        self.draw_tile_lines()
        # pygame.draw.circle(self.display_surface, 'red', self.origin, 10)
        self.preview()
        self.menu.display(self.selection_index)

#█████████████████████████████████████████████████████████     
class CanvasTile:
    def __init__(self, tile_id, offset = vector()):
        
        # Terrain
        self.has_terrain = False
        self.terrain_neighbors = []

        # Water
        self.has_water = False
        # animation of surface of water
        self.water_on_top = False

        # Coin
        self.coin = None

        # Enemy
        self.enemy = None

        # Objects
        self.objects = []

        self.add_id(tile_id, offset= offset)
        self.is_empty = False

    def add_id(self, tile_id, offset= vector()):
        # new options dictionary
        options = {key: value['style'] for key, value in EDITOR_DATA.items()}
        match options[tile_id]:
            case 'terrain': self.has_terrain = True
            case 'water': self.has_water = True
            case 'coin': self.coin = tile_id
            case 'enemy': self.enemy = tile_id
            # like else, to work with objects
            case _:
                if (tile_id, offset) not in self.objects:
                    self.objects.append((tile_id, offset))

    def remove_id(self, tile_id):
        options = {key: value['style'] for key, value in EDITOR_DATA.items()}
        match options[tile_id]:
            case 'terrain': self.has_terrain = False
            case 'water': self.has_water = False
            case 'coin': self.coin = None
            case 'enemy': self.enemy = None
        self.check_content()

    def check_content(self):
        if not self.has_terrain and not self.has_water and not self.coin and not self.enemy:
            self.is_empty = True

    def get_water(self):
        return 'bottom' if self.water_on_top else 'top'
    
    def get_terrain(self):
        return ''.join(self.terrain_neighbors)


#█████████████████████████████████████████████████████████
class CanvasObject(pygame.sprite.Sprite):
    def __init__(self, pos, frames, tile_id, origin, group):
        super().__init__(group)
        self.tile_id = tile_id

        # Animation
        self.frames = frames
        self.frame_index = 0
        
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center= pos)

        # Movement
        self.distance_to_origin = vector(self.rect.topleft) - origin
        self.selected = False
        self.mouse_offset = vector()

    def start_drag(self):
        self.selected = True
        self.mouse_offset = vector(mouse_pos()) - vector(self.rect.topleft) 

    def drag(self):
        if self.selected:
            self.rect.topleft = mouse_pos() - self.mouse_offset

    def drag_end(self, origin):
        self.selected = False
        self.distance_to_origin = vector(self.rect.topleft) - origin

    def animate(self, dt):
         self.frame_index += ANIMATION_SPEED * dt
         self.frame_index = 0 if self.frame_index >= len(self.frames) else self.frame_index
         self.image = self.frames[int(self.frame_index)]
         self.rect = self.image.get_rect(midbottom= self.rect.midbottom)

    def pan_pos(self, origin):
        self.rect.topleft = origin + self.distance_to_origin

    def update(self, dt):
        self.animate(dt)
        self.drag()

