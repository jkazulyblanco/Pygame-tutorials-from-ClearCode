from settings import *

class UpgradeMenu:
    def __init__(self,player):
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.attribute_number = len(player.stats)
        self.attribute_names = list(player.stats.keys())
        self.max_values = list(player.max_stats.values())
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # Item Creation
        self.height = screen_height * 0.8
        self.width = screen_width // 6
        self.create_items()
        # Selection system
        self.selection_index = 0

    # call in main by event key down
    def input_menu(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self.selection_index < self.attribute_number -1:
            self.selection_index += 1
        if keys[pygame.K_LEFT] and self.selection_index >= 1:
            self.selection_index -= 1
        if keys[pygame.K_SPACE]:
            self.item_list[self.selection_index].trigger(self.player)       

    def create_items(self):
        self.item_list = [] # invert
        for item,index  in enumerate(range(self.attribute_number)):
            increment = screen_width // self.attribute_number
            left = (item * increment) + (increment - self.width) // 2
            top = screen_height * 0.1
            item = Item(left,top,self.width,self.height,index,self.font)
            self.item_list.append(item)

    def display(self):
        for index, item in enumerate(self.item_list):
            # get attributes
            name = self.attribute_names[index]
            value = self.player.get_value_index(index)
            max_value = self.max_values[index]
            cost = self.player.get_cost_index(index)
            item.display_item(self.display_surface, self.selection_index,name,value,max_value,cost)
        

class Item:
    def __init__(self, l,t,w,h, index, font):
        self.rect = pygame.Rect(l,t,w,h)  
        self.index = index
        self.font = font

    def display_names(self, surface, name, cost, selected):
        # color
        color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR
        # title
        title_surf = self.font.render(name,False,color)
        title_rect = title_surf.get_rect(midtop= self.rect.midtop + vec2(0,20))
        # cost
        cost_surf = self.font.render(f'{int(cost)}',False,color)
        cost_rect = cost_surf.get_rect(midbottom= self.rect.midbottom + vec2(0,-20))
        # draw
        surface.blit(title_surf, title_rect)
        surface.blit(cost_surf, cost_rect)

    def display_bar(self, surface, value, max_value, selected):
        # drawing setup
        top = self.rect.midtop + vec2(0,60)
        bottom = self.rect.midbottom - vec2(0,60)
        color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR 
        # bar setup
        full_height = bottom[1] - top[1]
        relative_number = (value / max_value) * full_height
        value_rect = pygame.Rect(top[0]-15, bottom[1]-relative_number, 30, 10)
        # draw elements
        pygame.draw.line(surface,color,top,bottom,8)
        pygame.draw.rect(surface,color,value_rect)

    def trigger(self, player):
        upgrade_attribute = list(player.stats.keys())[self.index]
        if player.exp >= player.upgrade_cost[upgrade_attribute] and player.stats[upgrade_attribute] < player.max_stats[upgrade_attribute]:
            player.exp -= player.upgrade_cost[upgrade_attribute]
            player.stats[upgrade_attribute] *= 1.2
            player.upgrade_cost[upgrade_attribute] *= 1.4

        if player.stats[upgrade_attribute] > player.max_stats[upgrade_attribute]:
            player.stats[upgrade_attribute] = player.max_stats[upgrade_attribute]

    def display_item(self, surface, selection_num, name, value, max_value, cost):
        if self.index == selection_num:
            pygame.draw.rect(surface,'bisque3',self.rect)
            pygame.draw.rect(surface,UI_BORDER_COLOR_ACTIVE,self.rect,5)
        else:
            pygame.draw.rect(surface,UI_BG_COLOR,self.rect)
            pygame.draw.rect(surface,UI_BORDER_COLOR,self.rect,5)
        
        self.display_names(surface,name,cost,self.index==selection_num)
        self.display_bar(surface,value,max_value,self.index==selection_num)
