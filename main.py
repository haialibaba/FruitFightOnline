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
pygame.mixer.init()
pygame.mixer.music.load("assets/music/nhac_nen.mp3")
# Phát nhạc với số lần lặp lại là -1 để phát vô hạn
pygame.mixer.music.play(-1)
pygame.display.set_caption("GUN FIGHT")
throw_sound = pygame.mixer.Sound("assets/music/throw.mp3")
jump_sound = pygame.mixer.Sound("assets/music/jump_sound.mp3")
jump_sound.set_volume(0.08)  # Đặt âm lượng âm thanh là 50%
WIDTH, HEIGHT = 1000,640
FPS = 60
font_path = "assets/font/anta.ttf"
font_info = pygame.font.Font(font_path, 18)
Player_VEL = 5
speed_throw = 100
Player_name = "Hai"

chat_height = 300
chat_width = 400  # Chiều rộng của khung chat ít hơn một chút so với màn hình
chat_color = (0, 0, 0, 100)
chat_messages = []
chat_x = (WIDTH - chat_width) // 2
chat_y = (HEIGHT - chat_height) // 2
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

def draw_info_panel(window, player):
    # Thiết lập kích thước và màu sắc cho panel
    panel_height = 70
    panel_width = 180
    panel_color = (135, 206, 235, 150)  # Màu xanh da trời với độ trong suốt

    
    # Tạo một surface mới cho panel thông tin
    info_panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
    info_panel.fill(panel_color)
    
    # Thiết lập font và màu sắc cho text
    font = pygame.font.SysFont(None, 36)
    font_color = (50, 50, 50)  # Màu trắng

    image = pygame.image.load("assets//Background/images.jpg")  # Thay đổi đường dẫn tới hình ảnh của bạn
    image = pygame.transform.scale(image, (60, 60))
    # Vẽ thông tin lên panel
    lives_text = font_info.render("Lives: 10", True, font_color)
    bullets_text = font_info.render("Bullets: 10", True, font_color)

    # Đặt vị trí cho từng dòng text trên panel
    info_panel.blit(lives_text, (100, 5))
    info_panel.blit(bullets_text, (90, 35))
    info_panel.blit(image, (10, 5))
    
    # Vẽ panel lên window
    window.blit(info_panel, (5, 0))  # Bạn có thể thay đổi vị trí này tùy ý

def draw_chat_panel(window, input_text, input_visible):
    max_input_length = 35  # Giới hạn độ dài của văn bản nhập vào ô input
    
    if input_visible:  # Chỉ vẽ khung chat khi input_visible là True
        chat_panel = pygame.Surface((chat_width, chat_height), pygame.SRCALPHA)
        chat_panel.fill(chat_color)

        input_rect = pygame.Rect(chat_x + 10, chat_y + chat_height - 40, chat_width - 20, 30)
        pygame.draw.rect(window, (255, 255, 255), input_rect, 2)

        y_offset = 10
        for message in chat_messages:
            message_surface = font_info.render("You: " + message, True, (0, 0, 255))
            window.blit(message_surface, (chat_x + 10, chat_y + y_offset))
            y_offset += message_surface.get_height() + 5

        # Giới hạn độ dài của văn bản nhập vào ô input
        if len(input_text) > max_input_length:
            input_text = input_text[:max_input_length]

        # Vẽ `input_text` (nếu có)
        input_surface = font_info.render(input_text, True, (0, 0, 255))
        window.blit(input_surface, (chat_x + 20, chat_y + chat_height - 40 + 5))

        window.blit(chat_panel, (chat_x, chat_y))

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

def draw(window, background, bg_image,player,object,fruits,input_text,input_visible):
    for tiles in background:
        window.blit(bg_image, tiles)
    
    for obj in object:
        obj.draw(window)
        
    for fruit in fruits:
        fruit.draw(window)

    player.draw(window)
    draw_info_panel(window,player)
    draw_chat_panel(window,input_text,input_visible)
    pygame.display.update()

def load_map(block_size, background_image_path, custom_coordinates):
    background, bg_image = map.get_background(background_image_path)
    floor = [map.Block(x, y, block_size) for x, y in custom_coordinates]
    return background, bg_image, floor

def main(window):
    clock = pygame.time.Clock()
    player = character.Player(100, 100, 50, 50,Player_name)
    last_throw_time = pygame.time.get_ticks()
    is_throwing = False
    is_jumping = False
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
    input_text = ""
    typing_in_chat = False
    input_visible = False
    enter_pressed = False
    while run:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and player.jump_count < 2:
                    player.jump()
                    is_jumping = True
                elif event.key == pygame.K_SPACE:
                    if input_visible and typing_in_chat:  # Chỉ thêm dấu cách nếu đang nhập trong khung chat
                        input_text += " "
                    current_time = pygame.time.get_ticks()
                    if can_throw and not input_visible:
                        player.throw_fruit(fruits)
                        last_throw_time = current_time
                        is_throwing = True
                        can_throw = False

                elif event.key == pygame.K_TAB:  # Khi nhấn Tab
                    input_visible = not input_visible  # Đảo ngược giá trị của input_visible
                    typing_in_chat = input_visible
                elif input_visible:
                    if event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif event.key == pygame.K_RETURN:
                        chat_messages.append(input_text)
                        input_text = ""
                    elif event.key == pygame.K_SPACE:
                        if input_text and input_text[-1] != " ":
                            input_text += " "
                    else:
                        input_text += event.unicode     

        if is_jumping:
            jump_sound.play()
            is_jumping = False

        if is_throwing:
            throw_sound.play()
            is_throwing = False

        if not can_throw:
            current_time = pygame.time.get_ticks()
            if current_time - last_throw_time >= speed_throw:
                can_throw = True

        player.loop(FPS)    
        handle_move(player, floor)    
        draw(window, background, bg_image, player, floor, fruits,input_text,input_visible)  
        for fruit in fruits:
            fruit.rect.x += fruit.x_vel
            fruit.rect.y += fruit.y_vel
            if fruit.rect.right < 0 or fruit.rect.left > WIDTH:
                fruits.remove(fruit)  

    pygame.quit()
    quit()

if __name__ == "__main__":
    main(window)
