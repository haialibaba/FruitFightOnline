import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join
import character
import item
import map
pygame.init()

pygame.display.set_caption("GUN FIGHT")

WIDTH, HEIGHT = 1000,640
FPS = 60
Player_VEL = 5

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

def handle_vertical_colission(player,objects,dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player,obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
          

        collided_objects.append(obj)
    return collided_objects 

def handle_move(player,objects):
    keys = pygame.key.get_pressed()
    player.x_vel = 0
   
    if keys[pygame.K_LEFT]:
        player.move_left(Player_VEL)
    if keys[pygame.K_RIGHT]:
        player.move_right(Player_VEL)

    handle_vertical_colission(player, objects, player.y_vel)

    player.rect.clamp_ip(window.get_rect())

def draw(window, background, bg_image,player,object,fruits):
    for tiles in background:
        window.blit(bg_image, tiles)
    
    for obj in object:
        obj.draw(window)
        
    for fruit in fruits:
        fruit.draw(window)

    player.draw(window)
    pygame.display.update()

def load_map(block_size, background_image_path, custom_coordinates):
    background, bg_image = map.get_background(background_image_path)
    floor = [map.Block(x, y, block_size) for x, y in custom_coordinates]
    return background, bg_image, floor

def main(window):
    clock = pygame.time.Clock()
    player = character.Player(100, 100, 50, 50)
    last_throw_time = pygame.time.get_ticks()
    can_throw = True
    fruits = []

    block_size = 66
    background, bg_image, floor = load_map(block_size, "BG_galaxy.jpg", 
                                           [(70, 200), (137, 200), (204, 200), (500, 200), 
                                            (566, 200), (633, 200), (923, 200), (200, 350), 
                                            (267, 350), (750, 350), (813, 350), (879, 350), 
                                            (30, 500), (400, 500), (466, 500), (533, 500), 
                                            (600, 500)])

    run = True
    while run:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and player.jump_count < 2:
                    player.jump()
                elif event.key == pygame.K_SPACE:
                    current_time = pygame.time.get_ticks()
                    if can_throw:
                        player.throw_fruit(fruits)
                        last_throw_time = current_time
                        can_throw = False
               
        if not can_throw:
            current_time = pygame.time.get_ticks()
            if current_time - last_throw_time >= 100:
                can_throw = True

        player.loop(FPS)    
        handle_move(player, floor)    
        draw(window, background, bg_image, player, floor, fruits)  

        for fruit in fruits:
            fruit.rect.x += fruit.x_vel
            fruit.rect.y += fruit.y_vel
            # Kiểm tra xem quả táo có ra khỏi màn hình không, nếu có thì loại bỏ nó khỏi danh sách
            if fruit.rect.right < 0 or fruit.rect.left > WIDTH:
                fruits.remove(fruit)  

    pygame.quit()
    quit()

if __name__ == "__main__":
    main(window)
