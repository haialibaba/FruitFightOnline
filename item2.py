# import os
# import random
# import math
# import pygame
# from os import listdir
# from os.path import isfile, join
# import main
# import map
# pygame.init()

# class Fruit(pygame.sprite.Sprite):
#     def __init__(self, x, y, width, height, Fruit_name):
#         super().__init__()
#         self.rect = pygame.Rect(x, y, width, height)
#         self.x_vel = 0
#         self.y_vel = 0
#         self.Fruit_name = Fruit_name
#         self.update_image()  # Cập nhật hình ảnh ban đầu khi khởi tạo

#     def update_image(self):
#         # Cập nhật hình ảnh dựa trên Fruit_name
#         self.image = self.load_sprite_sheet("Items", "Fruits", self.Fruit_name, self.rect.width, self.rect.height)

#     def draw(self, window):
#         window.blit(self.image, self.rect)

#     def load_sprite_sheet(self, dir1, dir2, Fruit_name, width, height):
#         path = os.path.join("assets", dir1, dir2)
#         filename = Fruit_name + ".png"  
#         full_path = os.path.join(path, filename)
#         sprite_sheet = pygame.image.load(full_path).convert_alpha()
#         sprite = pygame.Surface((width, height), pygame.SRCALPHA, 32)
#         sprite.blit(sprite_sheet, (0, 0))
#         scaled_sprite = pygame.transform.scale(sprite, (width * 2, height * 2))

#         return scaled_sprite


import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join
import main
import map
pygame.init()

name_fruit="Melon"
class Fruit(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height,Fruit_name):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.Fruit_name = Fruit_name
        sprites = self.load_sprite_sheet("Items", "Fruits", width, height) 
        self.image = sprites[Fruit_name]  

    def draw(self, window):
        window.blit(self.image, self.rect)

    def load_sprite_sheet(self, dir1, dir2, width, height):  # Thêm width và height vào đây
        path = join("assets", dir1, dir2)
        images = [f for f in listdir(path) if isfile(join(path, f))]
        all_sprites = {}

        for image in images:
            sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()
            sprite = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            sprite.blit(sprite_sheet, (0, 0))
            scaled_sprite = pygame.transform.scale(sprite, (width * 2, height * 2))  # Scale sprite lên gấp đôi
            all_sprites[image.replace(".png", "")] = scaled_sprite

        return all_sprites
        