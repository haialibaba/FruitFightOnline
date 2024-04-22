import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join
import player_offline
import player_offline_2
import item
import map
import datetime
import lose
import win
pygame.init()
# pygame.mixer.init()
# pygame.mixer.music.load("assets/music/nhac_nen.mp3")
# pygame.mixer.music.play(-1)
pygame.display.set_caption("GUN FIGHT")
throw_sound = pygame.mixer.Sound("assets/music/throw.mp3")
jump_sound = pygame.mixer.Sound("assets/music/jump_sound.mp3")
jump_sound.set_volume(0.08)  # Đặt âm lượng âm thanh là 50%
WIDTH, HEIGHT = 1000,640
FPS = 60
font_path = "assets/font/anta.ttf"
font_info = pygame.font.Font(font_path, 18)
Player_VEL_1 = 5
speed_throw_1 = 100
Player_VEL_2 = 5
speed_throw_2 = 100
Player_name = "Hai"
chat_height = 300
chat_width = 400  # Chiều rộng của khung chat ít hơn một chút so với màn hình
chat_color = (0, 0, 0, 100)
initial_player1_lives = 15
initial_player2_lives = 15
font_player_name = pygame.font.Font(font_path, 24)
font_player_live = pygame.font.Font(font_path, 20)
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
    font_color = (50, 50, 50)  # Màu trắng

    image = pygame.image.load("assets/Background/images.jpg")  # Thay đổi đường dẫn tới hình ảnh của bạn
    image = pygame.transform.scale(image, (60, 60))

    image_heart = pygame.image.load("assets/Background/heart.png")  # Thay đổi đường dẫn tới hình ảnh của bạn
    image_heart = pygame.transform.scale(image_heart, (27, 27))
    # Vẽ thông tin lên panel
    lives_text = font_info.render("Lives: " + str(player.lives), True, font_color)
    name_text = font_player_name.render(player.name, True, font_color)

    info_panel.blit(name_text, (80, 2))
    # Đặt vị trí cho từng dòng text trên panel
    info_panel.blit(lives_text, (80, 35))
    info_panel.blit(image_heart, (152, 34))
    info_panel.blit(image, (10, 5))
    
    # Vẽ panel lên window
    window.blit(info_panel, (5, 0))  # Bạn có thể thay đổi vị trí này tùy ý

def draw_info_panel2(window, player2):
    panel_height = 70
    panel_width = 180
    panel_color = (135, 206, 235, 150)  # Màu xanh da trời với độ trong suốt
    
    # Tạo một surface mới cho panel thông tin
    info_panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
    info_panel.fill(panel_color)
    
    # Thiết lập font và màu sắc cho text
    font_color = (50, 50, 50)  # Màu trắng

    image = pygame.image.load("assets//Background/images.jpg")  # Thay đổi đường dẫn tới hình ảnh của bạn
    image = pygame.transform.scale(image, (60, 60))

    image_heart = pygame.image.load("assets//Background/heart.png")  # Thay đổi đường dẫn tới hình ảnh của bạn
    image_heart = pygame.transform.scale(image_heart, (27, 27))
    # Vẽ thông tin lên panel
    lives_text = font_info.render("Lives: " + str(player2.lives), True, font_color)
    name_text = font_player_name.render(player2.name, True, font_color)

    info_panel.blit(name_text, (75, 2))
    # Đặt vị trí cho từng dòng text trên panel
    info_panel.blit(lives_text, (80, 35))
    info_panel.blit(image_heart, (152, 34))
    info_panel.blit(image, (10, 5))
    
    # Vẽ panel lên window
    window.blit(info_panel, (818, 0))  # Bạn có thể thay đổi vị trí này tùy ý

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
        player.move_left(Player_VEL_1)
    if keys[pygame.K_RIGHT]:
        player.move_right(Player_VEL_1)

    handle_vertical_colission(player, objects, player.y_vel)

    player.rect.clamp_ip(window.get_rect())

def handle_move2(player,objects):
    keys = pygame.key.get_pressed()
    player.x_vel = 0
   
    handle_vertical_colission(player, objects, player.y_vel)

    player.rect.clamp_ip(window.get_rect())

def draw(window, background, bg_image,player,player2,object,fruits1, fruits2,boxes):
    for tiles in background:
        window.blit(bg_image, tiles)
    
    for obj in object:
        obj.draw(window)
        
    for fruit1 in fruits1:
        fruit1.draw(window)

    for fruit2 in fruits2:
        fruit2.draw(window)

    player.draw(window)
    player2.draw(window)
    draw_info_panel(window,player)
    draw_info_panel2(window,player2)
    if boxes is not None:
        boxes.draw(window)
    pygame.display.update()


maps_array = [
    {"bg_image": "BG_galaxy.jpg", 
     "floor": [(30, 270), (96, 270), (162, 270), (500, 270), 
               (566, 270), (633, 270), (923, 270), 
               (200, 430),(267, 430), (750, 430), (813, 430), (879, 430), 
               (0, 580), (66, 580), (132, 580), (198, 580),(264,580),(330,580),(396,580),(462,580),(528,580),(594,580),(660,580),(726,580), (792, 580),(858, 580),(924, 580),(990, 580),(1056, 580)],
        "block_y": 0},
    {"bg_image": "forest.jpg", 
     "floor": [  (76, 200),(280,120), (650, 150), (850, 270),
               (450,300), 
               (200, 430), (720, 430), 
            (0, 580), (66, 580), (132, 580), (198, 580),(264,580),(330,580),(396,580),(462,580),(528,580),(594,580),(660,580),(726,580), (792, 580),(858, 580),(924, 580),(990, 580),(1056, 580)],
     "block_y": 0},

    {"bg_image": "BG_sea.jpg", 
     "floor": [ (10, 270), (76, 270),(449, 270), (516, 270), (850, 270), (916, 270), 
               (240, 430), (690, 430), 
               (0, 580), (66, 580), (132, 580), (198, 580),(264,580),(330,580),(396,580),(462,580),(528,580),(594,580),(660,580),(726,580), (792, 580),(858, 580),(924, 580),(990, 580),(1056, 580)],
    "block_y": 134 },

    
    {"bg_image": "BG_samac.jpg", 
     "floor": [ (120, 270), (186, 270),(252, 270), (620, 270), (686, 270), (752, 270), 
               (400, 430),(466,430), (850, 430), 
               (0, 580), (66, 580), (132, 580), (198, 580),(264,580),(330,580),(396,580),(462,580),(528,580),(594,580),(660,580),(726,580), (792, 580),(858, 580),(924, 580),(990, 580),(1056, 580)],
       "block_y": 68}

]

def load_map(block_size, map_info):
    background_image_path = map_info["bg_image"]
    custom_coordinates = map_info["floor"]
    block_y = map_info.get("block_y", 0)
    background, bg_image = map.get_background(background_image_path)
    floor = [map.Block(x, y, block_size,block_y) for x, y in custom_coordinates]
    return background, bg_image, floor

def speed_fruit(fruits):
    if fruits == "Papple" :
        speed = 10
    elif fruits == "Kiwi" or fruits == "Bananas" or fruits == "Pineapple" or fruits == "Pstrawberry":
        speed = 15
    elif fruits == "Melon":
        speed = 6
    elif fruits == "Orange":
        speed = 17
    elif fruits == "Pcherries":
        speed = 22
    return speed

def damge_fruit(fruits):
    if fruits == "Papple" or fruits == "Kiwi" or fruits == "Orange" or fruits == "Bananas":
        damge = 1
    elif fruits == "Melon":
        damge = 3
    elif fruits == "Pcherries":
        damge = 1 
    elif fruits == "Pineapple" or fruits == "Pstrawberry":
        damge = 2  
    return damge

def throw_fruit(player, fruits):
    initial_speed = speed_fruit(player.Fruit_name)
    speed_increment = 1
    if player.direction == "left":
        fruit = item.Fruit(player.rect.left, player.rect.top, 32, 32,player.Fruit_name)
        fruit.x_vel = -initial_speed  # Thiết lập vận tốc ban đầu của quả táo khi ném sang trái
    elif player.direction == "right":
        fruit = item.Fruit(player.rect.right, player.rect.top, 32, 32,player.Fruit_name)
        fruit.x_vel = initial_speed   # Thiết lập vận tốc ban đầu của quả táo khi ném sang phải

    initial_speed += speed_increment
    fruits.append(fruit)

def main(window, chosen_character1, chosen_character2, name1, name2,lives):
    global initial_player1_lives, initial_player2_lives
    clock = pygame.time.Clock()
    player = player_offline.Player(100, 100, 50, 50,name1,'Papple',initial_player1_lives)
    player2 = player_offline_2.Player(700, 700, 50, 50,name2,'Papple',initial_player2_lives)
    last_throw_time = pygame.time.get_ticks()
    is_throwing = False
    is_jumping = False
    can_throw1 = True
    can_throw2 = True
    fruits1 = []
    fruits2 = []

    fruits_random_array = ["Papple", "Bananas","Pcherries","Pstrawberry", "Kiwi", "Melon", "Orange", "Pineapple"]

    current_time = datetime.datetime.now()
    hour_time = datetime.datetime.now().hour
    # Trích xuất số phút từ thời gian hiện tại
    current_minute = current_time.minute
    # Tính giá trị dựa trên số phút
    my_value = (current_minute % 4) + 1

    box = map.Box((current_minute * my_value) / hour_time, ( current_minute * hour_time) / my_value, 45)

    block_size = 66
    random_map_info = random.choice(maps_array)
    background, bg_image, floor = load_map(block_size, random_map_info)

    run = True
    last_box_touch_time = None
    input_visible = False
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
                    current_time = pygame.time.get_ticks()
                    if can_throw1 and not input_visible:
                        throw_fruit(player,fruits1)
                        last_throw_time = current_time
                        is_throwing = True
                        can_throw1 = False
                elif event.key == pygame.K_RETURN:
                    current_time = pygame.time.get_ticks()
                    if can_throw2 and not input_visible:
                        throw_fruit(player2,fruits2)
                        last_throw_time = current_time
                        is_throwing = True
                        can_throw2 = False

        if is_jumping:
            jump_sound.play()
            is_jumping = False

        if is_throwing:
            throw_sound.play()
            is_throwing = False

        if not can_throw2:
            current_time = pygame.time.get_ticks()
            if current_time - last_throw_time >= speed_throw_1:
                can_throw2 = True

        if not can_throw1:
            current_time = pygame.time.get_ticks()
            if current_time - last_throw_time >= speed_throw_2:
                can_throw1 = True

        player.loop(FPS)
        player2.loop(FPS)    
        handle_move(player, floor)
        handle_move2(player2, floor)

        # Bot action directly integrated into main
        distance_x = player.rect.x - player2.rect.x
        distance_y = player.rect.y - player2.rect.y
        if abs(distance_x) > 300:
            if distance_x < 0 or distance_y > 0:
                player2.move_left(Player_VEL_2)
            elif distance_x > 0 or distance_y < 0:
                player2.move_right(Player_VEL_2)
        elif abs(distance_y) > 50 and abs(distance_x) > 0 and player2.jump_count < 2:
            player2.jump()
        elif abs(distance_x) <= 400:
            current_time = pygame.time.get_ticks()
            if current_time - last_throw_time >= 500:
                if distance_x < 0:
                    player2.move_left(Player_VEL_2)
                # Quay qua phải nếu distance_x là giá trị dương
                else:
                    player2.move_right(Player_VEL_2)
                throw_fruit(player2, fruits2)
                last_throw_time = current_time

        if box is not None and box.rect.colliderect(player.rect):
            print("Player 1 touched the box")
            last_box_touch_time = pygame.time.get_ticks()
            box = None
            random_fruit = random.choice(fruits_random_array)
            player.Fruit_name = random_fruit

        if box is not None and box.rect.colliderect(player2.rect):
            print("Player 2 touched the box")
            last_box_touch_time = pygame.time.get_ticks()
            box = None
            random_fruit = random.choice(fruits_random_array)
            player2.Fruit_name = random_fruit
                            
        if last_box_touch_time is not None and pygame.time.get_ticks() - last_box_touch_time >= 20000:
            new_box_x = (player.rect.x + player2.rect.x) / 2
            new_box_y = (player.rect.y + player2.rect.y) / 2  
            box = map.Box(new_box_x, new_box_y, 45)
            last_box_touch_time = pygame.time.get_ticks()    

        draw(window, background, bg_image, player,player2, floor, fruits1,fruits2,box)  
        for fruit in fruits1:
            fruit.rect.x += fruit.x_vel
            fruit.rect.y += fruit.y_vel
            distance_x = fruit.rect.x - player2.rect.x
            distance_y = fruit.rect.y - player2.rect.y
            if abs(distance_x) < 200 and abs(distance_y) < 200 and player2.jump_count < 2:
                # Nếu đạn gần chạm player2 và player2 có thể nhảy, player2 nhảy lên
                player2.jump()
            if fruit.rect.right < 0 or fruit.rect.left > WIDTH:
                fruits1.remove(fruit)
            elif fruit.rect.colliderect(player2.rect):
                initial_player2_lives -= damge_fruit(player.Fruit_name)
                fruits1.remove(fruit)
                pygame.display.update()
        player2.lives = initial_player2_lives

        for fruit in fruits2:
            fruit.rect.x += fruit.x_vel
            fruit.rect.y += fruit.y_vel
            if fruit.rect.right < 0 or fruit.rect.left > WIDTH:
                fruits2.remove(fruit)
            if fruit.rect.colliderect(player.rect):
                initial_player1_lives -= damge_fruit(player2.Fruit_name)
                fruits2.remove(fruit)
                pygame.display.update()
        player.lives = initial_player1_lives

        if initial_player1_lives <= 0:
            pygame.mixer.music.stop()
            win.main_menu("WIN","BOT",chosen_character2)
            initial_player1_lives = lives
            initial_player2_lives = lives
            pygame.quit()
            quit()
        elif initial_player2_lives <= 0:
            pygame.mixer.music.stop()
            win.main_menu("WIN",name1,chosen_character1)
            initial_player1_lives = lives
            initial_player2_lives = lives
            pygame.quit()
            quit() 

    pygame.quit()
    quit()

if __name__ == "__main__":
    main(window, "PinkMan", "NinjaFrog","Hai","Kha",15)

