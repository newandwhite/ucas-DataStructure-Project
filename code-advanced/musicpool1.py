import pygame
import random
from os import walk
from opern import *
import time

# initialize pygame
pygame.init()
pygame.mixer.init()

# game window
screen_width = 1110
screen_height = 800

# # Sound
# drop_sound = pygame.mixer.Sound('drop.wav')

# create game window
screen = pygame.display.set_mode((screen_width,screen_height))
pool = pygame.Surface((screen_width, screen_height / 2))

pygame.display.set_caption('Night Pool with Colorful Rain(musical)')

# set frame rate
clock = pygame.time.Clock()
fps = 60

# game variables
drop_size = [{'S':5},
            {'S':15},
            {'S':50}]
drop_speed = [{'S':0},
            {'S':5}]
flash = False
windy = False
current_time = 0
button_press_time = 0

# color
PANEL = (184,66,66)
WHITE =  (255, 255, 255)
BLACK = (40,40,70)
# BLUE = (70,70,120)
NIGHT = (130,130,130)
GREEN = (40, 80, 60)

#timer
T1 = 12

# Lotus type
lotus_seq = [{'T':'f3u', 'X':10, 'Y':450},
            {'T':'g3', 'X':110, 'Y':450},
            {'T':'a3', 'X':210, 'Y':450},
            {'T':'b3', 'X':310, 'Y':450},
            {'T':'c4', 'X':410, 'Y':450},
            {'T':'d4', 'X':510, 'Y':450},
            {'T':'e4', 'X':610, 'Y':450},
            {'T':'f4', 'X':710, 'Y':450},
            {'T':'g4', 'X':810, 'Y':450},
            {'T':'b4', 'X':910, 'Y':450},
            {'T':'c5', 'X':1010, 'Y':450}
]

def import_folder(path):
    surface_list = []

    for _,__,img_files in walk(path):#the path to the file
        for image in img_files:
            full_path = path + '/' + image
            image_surf =  pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
    
    return surface_list

class Lightning(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.fog = pygame.Surface((screen_width, screen_height))
        self.fog.fill(NIGHT)
        self.light_mask = pygame.image.load('../graphics/light/light.png').convert_alpha()
        self.light_mask = pygame.transform.scale(self.light_mask, (screen_width,screen_height)) # change the size
        self.light_rect = self.light_mask.get_rect()
    
    # Assign the fog blit
    def render_fog(self):
        self.fog.fill(NIGHT)
        self.light_rect.center = (screen_width / 2, screen_height / 2)
        self.fog.blit(self.light_mask, self.light_rect)
        
    def render_dark(self):
        self.fog.fill(NIGHT)

class Thunder(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.frame_index = 0
        self.animation_speed = 0.7
        self.frames = import_folder('../graphics/flash')
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
    
    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 7
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()
        
class Water(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.frame_index = 0
        self.animation_speed = 0.2
        self.frames = import_folder('../graphics/water')
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = screen_height - 290

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()

class PartileEffect(pygame.sprite.Sprite):
    def __init__(self, pos, color):
        super().__init__()
        self.color = color
        self.frame_index = 0
        self.animation_speed = 0.4
        self.frames = import_folder('../graphics/splash')
        self.preimage = self.frames[self.frame_index]

        # Create mask
        self.splash_mask = pygame.mask.from_surface(self.preimage)
        self.splash_surf = self.splash_mask.to_surface()
        self.splash_surf.set_colorkey((0,0,0))

        # filling in the surface with a color
        surf_w, surf_h = self.splash_surf.get_size()
        for x in range(surf_w):
            for y in range(surf_h):
                if self.splash_surf.get_at((x, y))[0] != 0:
                    self.splash_surf.set_at((x,y), self.color) # go through and change every pixel
        
        self.image = self.splash_surf
        self.rect = self.image.get_rect(center = pos)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.preimage = self.frames[int(self.frame_index)]
             # Create mask
            self.splash_mask = pygame.mask.from_surface(self.preimage)
            self.splash_surf = self.splash_mask.to_surface()
            self.splash_surf.set_colorkey((0,0,0))

            # filling in the surface with a color
            surf_w, surf_h = self.splash_surf.get_size()
            for x in range(surf_w):
                for y in range(surf_h):
                    if self.splash_surf.get_at((x, y))[0] != 0:
                        self.splash_surf.set_at((x,y), self.color)
            self.image = self.splash_surf

    def update(self):
        self.animate()

class Lotus(pygame.sprite.Sprite):
    def __init__(self, counter):
        pygame.sprite.Sprite.__init__(self)
        self.frame_index = 0
        self.animation_speed = 0.11
        self.frames = import_folder('../graphics/lotus')
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.counter = counter
        self.rect.x = lotus_seq[self.counter]['X']
        self.rect.y = lotus_seq[self.counter]['Y']
    
    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()

class Ripple(pygame.sprite.Sprite):
    def __init__(self, color, x, y, radius):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.x = x
        self.y = y
        self.radius = radius
        self.image = pygame.Surface((screen_width, screen_height / 2))
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()

    def update(self):
        self.radius = self.radius + 1
        if self.radius > random.randint(30, 80):
            self.kill()

        self.image.fill(WHITE)
        pygame.draw.ellipse(screen, self.color, (self.x - self.radius*3/4, self.y - self.radius*3/8, self.radius*3/2, self.radius*3/4), 1)

class RainDrop(pygame.sprite.Sprite):
    def __init__(self, speedx):
        pygame.sprite.Sprite.__init__(self)
        self.color = (random.randint(50,255), random.randint(50,255), random.randint(50,255), random.randint(100,255))
        self.image = pygame.Surface((1,20))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.speedx = speedx
        self.speedy = random.randint(5,25)
        self.rect.x = random.randint(-100, screen_width)
        self.rect.y = random.randint(-screen_height, -5)
        self.radius = random.randint(2, 6)

    def update(self):
        self.rect.x = self.rect.x + self.speedx
        self.rect.y = self.rect.y + self.speedy

        if self.rect.bottom > random.randint((screen_height*14)//17, screen_height):
            ripple = Ripple(self.color, self.rect.x, self.rect.y, random.randint(2, 6))
            ripple_group.add(ripple)
            # drop_sound.play()
            self.kill()

class Player(pygame.sprite.Sprite):
    def __init__(self, speedx, posx):
        pygame.sprite.Sprite.__init__(self)
        self.color = (random.randint(50,255), random.randint(50,255), random.randint(50,255), random.randint(100,255))
        self.image = pygame.Surface((1,20))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.speedx = speedx
        self.speedy = 15
        self.rect.x = posx
        self.rect.y = -5
        self.radius = random.randint(2, 6) 

    def create_splash(self,pos):
        splash_sprite = PartileEffect(pos, self.color)
        splash_group.add(splash_sprite)
        
    def update(self):
        self.rect.x = self.rect.x + self.speedx
        self.rect.y = self.rect.y + self.speedy

        for l in lotus_group:
            if self.rect.colliderect(l.rect) and (self.rect.bottom < (screen_height*14)//17):
                self.create_splash((self.rect.x, self.rect.y))
                base_path = r'../node/wav/'  # r取消反/或者字符串中所有特殊含义的字符，还原本身含义
                path = base_path + lotus_seq[(self.rect.x - 10) // 100]['T'] + r'.wav'
                # Sound
                drop_sound = pygame.mixer.Sound(path)
                drop_sound.play()
                self.kill()

            elif self.rect.bottom > random.randint((screen_height*14)//17, screen_height):
                ripple = Ripple(self.color, self.rect.x, self.rect.y, random.randint(2, 6))
                ripple_group.add(ripple)
                # drop_sound.play()
                self.kill()

# Create sprite groups
raindrop_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
ripple_group = pygame.sprite.Group()
lotus_group = pygame.sprite.Group()
splash_group = pygame.sprite.GroupSingle()
water_group = pygame.sprite.Group()
light_group = pygame.sprite.Group()
thunder_group = pygame.sprite.Group()

water = Water()
water_group.add(water)
light = Lightning()
light_group.add(light)


for counter in range(0,11): # [)
    lotus = Lotus(counter)
    lotus_group.add(lotus)

node_count = 0
temp = -1   
timer1 = 0 
# game loop
run = True
while run:
    clock.tick(fps)

    current_time = pygame.time.get_ticks() # get current time
    keys = pygame.key.get_pressed()

    speedx = drop_speed[0]['S']
    # Wind animation
    if keys[pygame.K_w] and (windy == False):
        windy = True
        w_button = True
    if keys[pygame.K_s] and (windy == True):
        windy = False
        w_button = True
    if(windy == True):
        speedx = drop_speed[1]['S']
    if(windy == False):
        speedx = drop_speed[0]['S']

    val = 1
    # key control
    # use elif to avoid pressing two keys at the same time, which may lead to error
    # PgUp  
    if keys[pygame.K_UP] and (val < 2):
        val = val + 1
    # PgDn
    elif keys[pygame.K_DOWN] and (val > 0):
        val = val - 1

    # generate raindrops
    if len(raindrop_group) < drop_size[val]['S']:
        raindrop = RainDrop(speedx)
        raindrop_group.add(raindrop)
    # generate players
    # if len(player_group) < drop_size[val]['S']:
    #     player = Player(speedx)
    #     player_group.add(player)
    if timer1 < T1:
        timer1 += 1
    else:
        if node_count < len(opern):
            for n in range(0,int(len(node_pos)-1)):
                if opern[node_count] == node_pos[n]['name']:
                    temp = n
            if opern[node_count] == 'p':
                node_count += 1
            else:
                dropx = random.randint(node_pos[temp]['posl'], node_pos[temp]['posr'])
                player = Player(speedx, dropx)
                player_group.add(player)
                node_count += 1
        timer1 = 0
        

    # update platforms
    water.update()
    raindrop_group.update()
    player_group.update()
    lotus_group.update()
    
    # Draw background
    screen.fill(BLACK)
    
    # Draw water and lotus
    lotus_group.draw(screen)
    water_group.draw(screen)

    # Animation sprite update
    ripple_group.update()
    splash_group.update()
    
    # Draw on the screen 
    raindrop_group.draw(screen)
    player_group.draw(screen)
    ripple_group.draw(screen)
    splash_group.draw(screen)

    # Add night fog and lightning
    if keys[pygame.K_SPACE] and (flash == False):
        button_press_time = pygame.time.get_ticks()
        flash = True
        thunder = Thunder()
        thunder_group.add(thunder)
        

    if (flash == True):
        if current_time - button_press_time > 0:
            thunder.update()
            light.render_fog()
            thunder_group.draw(screen)
        if current_time - button_press_time > 100:
            light.render_dark()
        if current_time - button_press_time > 200:
            light.render_fog()
        if current_time - button_press_time > 300:
            light.render_dark()
            flash = False
            thunder.kill()
    else:
        flash = False
        light.render_dark()

    # Draw the light mask onto the fog image
    screen.blit(light.fog, (0, 0), special_flags = pygame.BLEND_MULT) # set blend mode

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # update display window
    pygame.display.update()

pygame.quit()