import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join
import main
pygame.init()

WIDTH, HEIGHT = 1000,640
FPS = 60
Player_VEL = 5

class Object(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height,name=None):
        super().__init__()
        self.rect = pygame.Rect(x,y, width, height)
        self.image = pygame.Surface((width,height),pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win):
        win.blit(self.image, (self.rect.x, self.rect.y))

def get_background(name):
    image =  pygame.image.load(join("assets","Background",name))
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)

    return tiles, image

def get_block(size,block_y):
    path = join("assets","Terrain","Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size,size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(96,block_y,size,size)
    surface.blit(image,(0,0),rect)
    return pygame.transform.scale2x(surface)

class Block(Object):
    def __init__(self,x,y,size,block_y): 
        super().__init__(x,y,size,size)
        block = get_block(size,block_y)
        self.image.blit(block, (0,0))
        self.mask = pygame.mask.from_surface(self.image)

def get_box(size):
    path = os.path.join("assets", "Items", "Boxes", "Box3", "Idle.png")
    try:
        box_image = pygame.image.load(path).convert_alpha()
        box_image = pygame.transform.scale(box_image, size)
        return box_image
    except pygame.error as e:
        print("Không thể tải ảnh từ:", path)
        print("Lỗi:", e)
        return None


class Box(Object):
    def __init__(self,x,y,size): 
        super().__init__(x,y,size,size)
        block = get_box((size, size))
        self.image.blit(block, (0,0))
        self.mask = pygame.mask.from_surface(self.image)



