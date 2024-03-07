import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join
import item
font_path = "assets/font/anta.ttf"
pygame.init()

WIDTH, HEIGHT = 1000,640
FPS = 60
Player_jump = 6
window = pygame.display.set_mode((WIDTH,HEIGHT))

def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

def load_sprite_sheet(dir1, dir2, width, height, direction = False):
    path = join ("assets",dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path,f))]
    all_sprites = {}
    
    for image in images:
        sprite_sheet = pygame.image.load(join(path,image)).convert_alpha()
        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height),pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0 ,width, height)
            surface.blit(sprite_sheet, (0,0), rect)
            sprites.append(pygame.transform.scale2x(surface))

        if direction:
            all_sprites[image.replace(".png","") + "_right"] = sprites   
            all_sprites[image.replace(".png","") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png","")] = sprites

    return all_sprites

class Player(pygame.sprite.Sprite):
    COLOR = (255,0,0)
    GRAVITY = 1
    SPRITES = load_sprite_sheet("MainCharacters","MaskDude", 32, 32, True)
    animation_delay = 3
    def __init__(self,x,y,width,height,name):
        super().__init__()
        #thiết lập giá trị va chạm
        self.rect = pygame.Rect(x,y,width,height)
        #tốc độ di chuyển người chơi
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.name = name
        self.font = pygame.font.SysFont('arial', 20)

    def jump(self):
        self.y_vel = -self.GRAVITY * Player_jump
        self.animation_count = 0
        self.jump_count += 1
        #double jump
        if self.jump_count == 1:
            self.fall_count = 0

    def move(self,dx,dy):
        self.rect.x += dx
        self.rect.y += dy

    def move_left(self,vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self,vel):   
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def loop(self,fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel,self.y_vel)
        self.fall_count += 1
        self.update_sprite()

    def throw_fruit(self, fruits):
        if self.direction == "left":
            fruit = item.Fruit(self.rect.left, self.rect.top, 32, 32)
            fruit.x_vel = -8  # Thiết lập vận tốc ban đầu của quả táo khi ném sang trái
        elif self.direction == "right":
            fruit = item.Fruit(self.rect.right, self.rect.top, 32, 32)
            fruit.x_vel = 8   # Thiết lập vận tốc ban đầu của quả táo khi ném sang phải
        fruits.append(fruit)

    def update_sprite(self):
        sprite_sheet =  "idle"
        if self.y_vel != 0:
            if self.jump_count == 1:
                sprite_sheet = "jump"
            if self.jump_count == 2:
                sprite_sheet = "double_jump"

        elif self.y_vel > self.GRAVITY * 2:
            sprite_sheet = "fall"

        elif self.x_vel != 0:
            sprite_sheet = "run"
        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.animation_delay) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()
        
    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)
    
    def draw_name(self, window):
        name_surface = self.font.render(self.name, True, (0, 0, 0))  # Tạo surface chứa tên
        name_x = self.rect.x + (self.rect.width - name_surface.get_width()) // 2
        name_y = self.rect.y - name_surface.get_height() - 5  
        window.blit(name_surface, (name_x, name_y))

    def draw(self,window):
        window.blit(self.sprite,(self.rect.x, self.rect.y))
        self.draw_name(window)
