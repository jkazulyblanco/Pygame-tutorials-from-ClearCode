# import pygame
from settings import *
from support import import_folder
from entity import Entity

class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack, create_magic):
        super().__init__(groups)
        self.image = pygame.image.load('../graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft= pos)       
        # inflate is like scale for rect
        self.hitbox = self.rect.inflate(-20, -26)

        # Graphics setup
        self.import_player_assets()
        self.status = 'down'
        # Movement
        self.speed = 5
        self.obstacle_sprites = obstacle_sprites
        # Timer
        self.attacking = False
        self.attack_cooldown = 200 # -----
        self.attack_time = None
        # Weapon
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.hightligh_weapon = False
        # Magic
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None
        self.hightligh_magic = False
        # Stats
        self.stats = {'health':100,'energy':60,'attack':10,'magic':4,'speed':6}
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.speed = self.stats['speed']
        # Upgrade Stats
        self.max_stats = {'health':300,'energy':140,'attack':20,'magic':10,'speed':10}
        self.upgrade_cost = {'health':100,'energy':100,'attack':100,'magic':100,'speed':100}
        self.exp = 1
        # Damage Timer
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerablility_duration = 500
        # Sound
        self.weapon_attack_sound = pygame.mixer.Sound('../audio/sword.wav')
        self.weapon_attack_sound.set_volume(0.4)

    # 🅰🅽🅸🅼🅰🆃🅸🅾🅽
    def import_player_assets(self):
        character_path = '../graphics/player/'
        self.animations = {'up':[],'down':[],'left':[],'right':[],
                           'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[],
                           'right_attack':[],'left_attack':[],'up_attack':[],'down_attack':[]}
        
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'
        # if attacking
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')    
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status: 
                self.status = self.status.replace('_attack', '')    
        
    def animate(self):
        # get keys from dict
        animation = self.animations[self.status]
        # loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        # set the image and update rect
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        # flickering
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    # 🅺🅴🆈 ​ 🅸🅽🅿🆄🆃
    def input(self):
        if not self.attacking:
            keys = pygame.key.get_pressed()
            # vertical movement
            if keys[pygame.K_w] and not keys[pygame.K_s]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_s] and not keys[pygame.K_w]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0
            # horizontal movement
            if keys[pygame.K_a] and not keys[pygame.K_d]:
                self.direction.x = -1
                self.status = 'left'
            elif keys[pygame.K_d] and not keys[pygame.K_a]:
                self.direction.x = 1
                self.status = 'right'
            else:
                self.direction.x = 0

    # Call in main by event pygame.KEYDOWN
    def attack_once(self):
        if not self.attacking:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_i]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
                self.weapon_attack_sound.play()
                # print('ATTACK ONE')
            
            if keys[pygame.K_o]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                style = list(magic_data.keys())[self.magic_index]
                strength = list(magic_data.values())[self.magic_index]['strength'] + self.stats['magic']
                cost = list(magic_data.values())[self.magic_index]['cost']
                self.create_magic(style, strength, cost)
                # print('MAGIC ONE')

            if keys[pygame.K_q]:
                self.weapon_change()
                self.hightligh_weapon = True
            
            if keys[pygame.K_e]:
                self.magic_change()
                self.hightligh_magic = True
                
    def weapon_change(self):
        self.weapon_index += 1
        if self.weapon_index >= len(list(weapon_data.keys())):
            self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
    
    def magic_change(self):
        self.magic_index += 1
        if self.magic_index >= len(list(magic_data.keys())):
            self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown + weapon_data[self.weapon]['cooldown']:
                self.attacking = False
                self.destroy_attack()

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerablility_duration:
                self.vulnerable = True

    def get_full_weapon_damage(self):
        base_damage = self.stats['attack']
        weapon_damage = weapon_data[self.weapon]['damage']
        return base_damage + weapon_damage
    
    def get_full_magic_damage(self):
        base_damage = self.stats['magic']
        spell_damage = magic_data[self.magic]['strength']
        return base_damage + spell_damage

    def energy_recovery(self):
        if self.energy < self.stats['energy']:
            self.energy += 0.1 * self.stats['magic']
        else:
            self.energy = self.stats['energy']

    def get_value_index(self, index):
        return list(self.stats.values())[index]

    def get_cost_index(self, index):
        return list(self.upgrade_cost.values())[index]

    def update(self):
        self.input() 
        self.cooldowns()
        self.animate()
        self.get_status()
        self.move(self.stats['speed'])
        self.energy_recovery()