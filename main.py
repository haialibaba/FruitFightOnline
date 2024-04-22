import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join
import character
import character2
import select_character
import item
import item2
import map
import lose
import win
import socket
import sys
import threading
import builtins
import itertools
import time
import datetime
pygame.init()

pygame.display.set_caption("GUN FIGHT1")
fruit_id_counter = itertools.count()
throw_sound = pygame.mixer.Sound("assets/music/throw.mp3")
jump_sound = pygame.mixer.Sound("assets/music/jump_sound.mp3")
dame_sound =pygame.mixer.Sound("assets/music/dame_sound.mp3")
jump_sound.set_volume(0.08)  # Đặt âm lượng âm thanh là 50%
WIDTH, HEIGHT = 1000,640
FPS = 60
font_path = "assets/font/anta.ttf"
font_info = pygame.font.Font(font_path, 18)
font_player_name = pygame.font.Font(font_path, 24)
font_player_live = pygame.font.Font(font_path, 20)
Player_VEL = 5
speed_throw = 500
Player_name = "Hai"
Player2_name = "Kha"
Player2_character="MaskDude"
Fruit_name = 'Papple'
Fruit_name_oponent = 'Papple'
chat_height = 300
chat_width = 400  # Chiều rộng của khung chat ít hơn một chút so với màn hình
chat_color = (0, 0, 0, 100)
chat_messages = []
chat_x = (WIDTH - chat_width) // 2
chat_y = (HEIGHT - chat_height) // 2
last_box_time = 0  # Thời gian cuối cùng box được vẽ
box_interval = 10000  # Khoảng thời gian giữa các lần vẽ box (10 giây)
initial_player1_lives = 10
initial_player2_lives = 10
count = 1
wait_image = pygame.image.load("assets/Background/wait_image.jpg")  # Thay đổi đường dẫn tới ảnh của bạn
wait_image = pygame.transform.scale(wait_image, (WIDTH, HEIGHT))
window = pygame.display.set_mode((WIDTH,HEIGHT))
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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

    info_panel.blit(name_text, (110, 2))
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

    info_panel.blit(name_text, (110, 2))
    # Đặt vị trí cho từng dòng text trên panel
    info_panel.blit(lives_text, (80, 35))
    info_panel.blit(image_heart, (152, 34))
    info_panel.blit(image, (10, 5))
    
    # Vẽ panel lên window
    window.blit(info_panel, (818, 0))  # Bạn có thể thay đổi vị trí này tùy ý

def draw_chat_panel(window, input_text, input_visible, scroll_offset):
    max_input_length = 35  # Giới hạn độ dài của văn bản nhập vào ô input
    line_height = font_info.get_height() + 5
    max_displayed_messages = ((chat_height - 20) // line_height)-1  # Số lượng tin nhắn tối đa hiển thị trên màn hình

    if input_visible:  # Chỉ vẽ khung chat khi input_visible là True
        chat_panel = pygame.Surface((chat_width, chat_height), pygame.SRCALPHA)
        chat_panel.fill(chat_color)

        input_rect = pygame.Rect(chat_x + 10, chat_y + chat_height - 40, chat_width - 20, 30)
        pygame.draw.rect(window, (255, 255, 255), input_rect, 2)

        # Xác định tin nhắn nào sẽ được hiển thị
        start_index = max(0, len(chat_messages) - max_displayed_messages - scroll_offset)
        end_index = len(chat_messages) - scroll_offset

        y_offset = 10
        for message in chat_messages[start_index:end_index]:
            message_surface = font_info.render(message, True, (0, 0, 255))
            window.blit(message_surface, (chat_x + 10, chat_y + y_offset))
            y_offset += line_height

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
        send_threada = threading.Thread(target=send_coordinate, args=(player.rect.x,player.rect.y))
        send_threada.start()
        
    if keys[pygame.K_RIGHT]:
        player.move_right(Player_VEL)
        send_threadv = threading.Thread(target=send_coordinate, args=(player.rect.x,player.rect.y))
        send_threadv.start()

    handle_vertical_colission(player, objects, player.y_vel)

    player.rect.clamp_ip(window.get_rect())

def handle_move2(player2,objects):
    
    handle_vertical_colission(player2, objects, player2.y_vel)

    player2.rect.clamp_ip(window.get_rect())

def draw(window, background, bg_image,player,player2,object,fruits,fruit_opponent,boxes,input_text,input_visible,scroll_offset,fruits2):
    pygame.event.pump()
    for tiles in background:
        window.blit(bg_image, tiles)
    
    for obj in object:
        obj.draw(window)

    for fruit in fruits:
        fruit.draw(window)

    for fruit2 in fruits2:
        fruit2.draw(window)

    
    player.draw(window)
    player2.draw(window)
    draw_info_panel(window,player)
    draw_info_panel2(window,player2)
    draw_chat_panel(window,input_text,input_visible,scroll_offset)
    if boxes is not None:
        boxes.draw(window)
    pygame.display.update()



############################################

def connect_to_server(server_ip, server_port):
    try:
        client_socket.connect((server_ip, server_port))
        print("Kết nối thành công!")
    except Exception as e:
        print("Không thể kết nối đến server:", e)
        sys.exit(1) 

def close_connection():
    client_socket.close()

def send_coordinate(player_x,player_y):
    data = f"COORD:{player_x} {player_y}|"
    client_socket.send(data.encode())

        
def send_name_info(name):
        name_info = f"NAME_INFO:{name}|"
        client_socket.send(name_info.encode())

def send_info_fruit(fruit_name):
    fruit_info  = f"FRUIT_NAME:{fruit_name}|"
    client_socket.send(fruit_info.encode())

def get_unique_fruit_id():
    return next(fruit_id_counter)

def send_coordinate_Fruit(fruit_x,fruit_y):
        fruit_id = get_unique_fruit_id()
        data = f"COORD_FRUIT:{fruit_x} {fruit_y}|"
        client_socket.send(data.encode())

def send_chat(chat):
        chat = f"CHAT:{chat}|"
        client_socket.send(chat.encode())
   
def send_character_info(character):
        name_info = f"CHARACTER_INFO:{character}|"
        client_socket.send(name_info.encode())
      
def send_sprite_info(sprite_sheet):
        sprite_info = f"SPRITE:{sprite_sheet}|"
        client_socket.send(sprite_info.encode())
       

def receive_thread(player2,fruit_opponent,callback,player1,fruits2):
    data = client_socket.recv(1024).decode().split('\n')
    result = []
    fruit_data = []
    global initial_player1_lives
    global map_id 
    for line in data:
        parts = []
        current_part = ''
        for char in line:
            if char == 'C' or char == 'S'or char == 'A': 
                if current_part:
                    parts.append(current_part)
                current_part = char
            else:
                current_part += char
        if current_part:
            parts.append(current_part)
        result.append(parts)
    for group in result:
        for item in group:
            if item.startswith("COORD:"):
                coord_data = item[6:] 
                x, y = builtins.map(int, coord_data.split())
                player2.rect.x, player2.rect.y = x, y
            elif item.startswith("AME_INFO:"):
                player2.name = item[9:]
            elif item.startswith("CTER_INFO:"):
                if "VirtualGuy" in item :
                    player2_character = "VirtualGuy"
                    player2.SPRITES = character2.load_sprite_sheet("MainCharacters", player2_character, 32, 32, True)
                elif "MaskDude" in item :
                    player2_character = "MaskDude"
                    player2.SPRITES = character2.load_sprite_sheet("MainCharacters", player2_character, 32, 32, True)
                elif "NinjaFrog" in item :
                    player2_character = "NinjaFrog"
                    player2.SPRITES = character2.load_sprite_sheet("MainCharacters", player2_character, 32, 32, True)
                elif "PinkMan" in item :
                    player2_character = "PinkMan"
                    player2.SPRITES = character2.load_sprite_sheet("MainCharacters", player2_character, 32, 32, True)
            elif item.startswith("SPRITE:"):
                sprite = item[7:]
                player2.double_jump = sprite
            elif item.startswith("AT:"):
                chat = item[3:]
                chat_messages.append(player2.name + ":" + chat)
            elif item.startswith("AME:"):
                Fruit_name = item[4:]
                player2.Fruit_name = Fruit_name
                fruit_opponent.Fruit_name = Fruit_name
                callback(Fruit_name)
            elif item.startswith("COORD_FRUIT:"):
                coord_data = item[12:]
                x, y = builtins.map(int, coord_data.split())
                if coord_data is not None:
                    throw_fruit2(player2,fruits2)

                # time.sleep(0.5)
                # if fruit_opponent.rect.colliderect(player1.rect):
                #     fruit_opponent.rect.x, fruit_opponent.rect.y = 999,999
                #     dame_sound.play()
                #     time.sleep(0.5)
                #     initial_player1_lives -= damge_fruit(player2.Fruit_name)
                #     print("Player 2 hits player 1")
                #     pygame.display.update()

                # player1.lives = initial_player1_lives
                

def speed_fruit(fruits):
    if fruits == "Papple" :
        speed = 25
    elif fruits == "Kiwi" or fruits == "Bananas" or fruits == "Pineapple" or fruits == "Pstrawberry":
        speed = 25
    elif fruits == "Melon":
        speed = 25
    elif fruits == "Orange":
        speed = 25
    elif fruits == "Pcherries":
        speed = 25
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
        fruit = item.Fruit(player.rect.left, player.rect.top, 32, 32, player.Fruit_name)
        fruit.x_vel = - initial_speed  # Thiết lập vận tốc ban đầu của quả táo khi ném sang trái
    elif player.direction == "right":
        fruit = item.Fruit(player.rect.right, player.rect.top, 32, 32, player.Fruit_name)
        fruit.x_vel = initial_speed  # Thiết lập vận tốc ban đầu của quả táo khi ném sang phải
        
    initial_speed += speed_increment
    fruits.append(fruit)
    
    return fruit

def throw_fruit2(player2, fruits2):
    initial_speed = speed_fruit(player2.Fruit_name)
    speed_increment = 1
    if player2.direction == "left":
        fruit2 = item2.Fruit(player2.rect.left, player2.rect.top, 32, 32, player2.Fruit_name)
        fruit2.x_vel = - initial_speed  # Thiết lập vận tốc ban đầu của quả táo khi ném sang trái
    elif player2.direction == "right":
        fruit2 = item2.Fruit(player2.rect.right, player2.rect.top, 32, 32, player2.Fruit_name)
        fruit2.x_vel = initial_speed  # Thiết lập vận tốc ban đầu của quả táo khi ném sang phải
        
    initial_speed += speed_increment
    fruits2.append(fruit2)
    
    return fruit2

maps_array = [
    {
        "id": 1,
        "bg_image": "BG_galaxy.jpg",
        "floor": [(30, 270), (96, 270), (162, 270), (500, 270), 
               (566, 270), (633, 270), (923, 270), 
               (200, 430),(267, 430), (750, 430), (813, 430), (879, 430), 
               (0, 580), (66, 580), (132, 580), (198, 580),(264,580),(330,580),(396,580),(462,580),(528,580),(594,580),(660,580),(726,580), (792, 580),(858, 580),(924, 580),(990, 580),(1056, 580)],
        "block_y": 0
    },
    {
        "id": 2,
        "bg_image": "forest.jpg",
        "floor": [  (76, 200),(280,120), (650, 150), (850, 270),
                    (450,300), 
                    (200, 430), (720, 430), 
                    (0, 580), (66, 580), (132, 580), (198, 580),(264,580),(330,580),(396,580),(462,580),(528,580),(594,580),(660,580),(726,580), (792, 580),(858, 580),(924, 580),(990, 580),(1056, 580)],
        "block_y": 0
    },
    {
        "id": 3,
        "bg_image": "BG_sea.jpg",
        "floor": [ (10, 270), (76, 270),(449, 270), (516, 270), (850, 270), (916, 270), 
               (240, 430), (690, 430), 
               (0, 580), (66, 580), (132, 580), (198, 580),(264,580),(330,580),(396,580),(462,580),(528,580),(594,580),(660,580),(726,580), (792, 580),(858, 580),(924, 580),(990, 580),(1056, 580)],
        "block_y": 134
    },
    {
        "id": 4,
        "bg_image": "BG_samac.jpg",
        "floor": [ (120, 270), (186, 270),(252, 270), (620, 270), (686, 270), (752, 270), 
               (400, 430),(466,430), (850, 430), 
               (0, 580), (66, 580), (132, 580), (198, 580),(264,580),(330,580),(396,580),(462,580),(528,580),(594,580),(660,580),(726,580), (792, 580),(858, 580),(924, 580),(990, 580),(1056, 580)],
        "block_y": 68
    }
]


def load_map(block_size, map_id):
    for map_info in maps_array:
        if map_info["id"] == map_id:
            background_image_path = map_info["bg_image"]
            custom_coordinates = map_info["floor"]
            block_y = map_info.get("block_y", 0)
            background, bg_image = map.get_background(background_image_path)
            floor = [map.Block(x, y, block_size, block_y) for x, y in custom_coordinates]
            return background, bg_image, floor


def calculate_seconds():
    current_seconds = int(time.time() % 60)

    if current_seconds >= 1 and current_seconds <= 10:
        result = current_seconds / 10 * 0.5 + 0.5  # Chuyển từ khoảng từ 0 đến 1 thành khoảng từ 0.5 đến 1
    elif current_seconds >= 11 and current_seconds <= 60:
        result = current_seconds / 100 * 0.5 + 0.5  # Chuyển từ khoảng từ 0 đến 1 thành khoảng từ 0.5 đến 1

    return result



def receive_client_count_from_server(name,chosen_character,fruit_name):
    global count  # Đảm bảo rằng biến count được gọi từ phạm vi toàn cục
    while True:
        try:
            client_count_data = client_socket.recv(1024).decode()
            if not client_count_data:
                break
            if "SERVER_CLIENT_COUNT:" in client_count_data:
                count_str = client_count_data.split(":")[1]
                count = int(count_str)  
                if count == 1:
                    window.blit(wait_image, (0, 0))
                    pygame.display.flip()  
                elif count == 2:
                    result_variable = calculate_seconds()
                    time.sleep(result_variable)
                    receive_thread2lq = threading.Thread(target=send_name_info, args=(name,))
                    receive_thread2lq.start()

                    receive_thread2leq = threading.Thread(target=send_character_info, args=(chosen_character,))
                    receive_thread2leq.start()


        except Exception as e:
            print(f"Error receiving client count from server: {e}")
            break

##############################################################
def main(window, chosen_character, name,lives):
    pygame.mixer.music.stop()
    global initial_player1_lives, initial_player2_lives
    global count 
    connect_to_server("192.168.1.10", 80)  # Kết nối tới server khi bắt đầu chạy chương trình\
    try:
        clock = pygame.time.Clock()
        player = character.Player(100, 100, 50, 50,name,Fruit_name,initial_player1_lives)
        player2 = character2.Player2(750, 200, 50, 50, Player2_name, Player2_character,Fruit_name_oponent,initial_player2_lives)

        fruit_opponent = item2.Fruit(10000,10000,32,32,player2.Fruit_name)

        def handle(fruit_name):
            player2.Fruit_name = fruit_name
            fruit_opponent.update_image()
            return fruit_name
        
        last_throw_time = pygame.time.get_ticks()
        is_throwing = False
        is_jumping = False
        can_throw = True
        fruits = []
        fruits2 = []

        block_size = 66
        current_time = datetime.datetime.now()
        hour_time = datetime.datetime.now().hour
        # Trích xuất số phút từ thời gian hiện tại
        current_minute = current_time.minute
        # Tính giá trị dựa trên số phút
        my_value = (current_minute % 4) + 1
        background, bg_image, floor  = load_map(block_size,my_value)
        box = map.Box((current_minute * my_value) / hour_time, ( current_minute * hour_time) / my_value, 45)

        fruits_random_array = ["Papple", "Bananas","Pcherries","Pstrawberry", "Kiwi", "Melon", "Orange", "Pineapple"]
      

        run = True
        input_text = ""
        typing_in_chat = False
        input_visible = False
        last_box_touch_time = None
        scroll_offset = 0
        
        #count client
        receive_thread2l= threading.Thread(target=receive_client_count_from_server,args=(name,chosen_character,Fruit_name,))
        receive_thread2l.start()

        while run:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
                if event.type == pygame.USEREVENT:
                    if 'x' in event.dict and 'y' in event.dict and 'sprite' in event.dict :
                        x = event.dict['x']
                        y = event.dict['y']
                        sprite_sheet = event.dict['sprite']

                        send_thread1 = threading.Thread(target=send_coordinate, args=(x,y))
                        send_thread1.start()

                        send_thread1b = threading.Thread(target=send_sprite_info, args=(sprite_sheet,))
                        send_thread1b.start() 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:  # Cuộn lên
                        scroll_offset += 1
                    elif event.button == 5:  # Cuộn xuống
                        scroll_offset -= 1
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and player.jump_count < 2:
                        player.jump()
                        is_jumping = True
                    elif event.key == pygame.K_SPACE:
                        if input_visible and typing_in_chat:  # Chỉ thêm dấu cách nếu đang nhập trong khung chat
                            input_text += " "
                        current_time = pygame.time.get_ticks()
                        if can_throw and not input_visible:
                            throw_fruit(player, fruits)
                            last_throw_time = current_time
                            is_throwing = True
                            can_throw = False
                            for fruit in fruits:
                                send_thread_fruit = threading.Thread(target=send_coordinate_Fruit, args=(fruit.rect.x,fruit.rect.y))
                                send_thread_fruit.start()
                    if event.key == pygame.K_g and not input_visible:
                        pygame.mixer.music.stop()
                        lose.main_menu("LOSE",player.name,chosen_character)
                        initial_player1_lives = lives
                        initial_player2_lives = lives

                    elif event.key == pygame.K_TAB:  # Khi nhấn Tab
                        input_visible = not input_visible  # Đảo ngược giá trị của input_visible
                        typing_in_chat = input_visible
                    elif input_visible:
                        if event.key == pygame.K_BACKSPACE:
                            input_text = input_text[:-1]
                        elif event.key == pygame.K_RETURN:
                            chat_messages.append(player.name + ":" + input_text)
                            send_chatr = threading.Thread(target=send_chat, args=(input_text,))
                            send_chatr.start()
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
            player2.loop(FPS)
            handle_move(player, floor)
            handle_move2(player2,floor)

                    
            receive_threadx = threading.Thread(target=receive_thread, args=(player2,fruit_opponent,handle,player,fruits2 ))
            receive_threadx.start()

            
            for fruit in fruits:
                fruit.rect.x += fruit.x_vel
                fruit.rect.y += fruit.y_vel
                if fruit.rect.right < 0 or fruit.rect.left > WIDTH:
                    fruits.remove(fruit)
                    pygame.display.update()
                elif fruit.rect.colliderect(player2.rect):
                    dame_sound.play()
                    initial_player2_lives -= damge_fruit(player.Fruit_name)
                    print("Player 1 hit's player 2")
                    fruits.remove(fruit)
                    pygame.display.update()
            player2.lives = initial_player2_lives
          

            for fruit2 in fruits2:
                fruit2.rect.x += fruit2.x_vel
                fruit2.rect.y += fruit2.y_vel
                if fruit2.rect.right < 0 or fruit2.rect.left > WIDTH:
                    fruits2.remove(fruit2)
                    pygame.display.update()
                elif fruit2.rect.colliderect(player.rect):
                    dame_sound.play()
                    time.sleep(0.3)
                    initial_player1_lives -= damge_fruit(player2.Fruit_name)
                    print("Player 2 hit's player 1")
                    fruits2.remove(fruit2)
                    pygame.display.update()
            player.lives = initial_player1_lives

            if box is not None and box.rect.colliderect(player.rect):
                print("Player 1 touched the box")
                last_box_touch_time = pygame.time.get_ticks()
                box = None
                random_fruit = random.choice(fruits_random_array)
                player.Fruit_name = random_fruit
                receive_thread2_fruit = threading.Thread(target=send_info_fruit, args=(random_fruit,))
                receive_thread2_fruit.start()

            if box is not None and box.rect.colliderect(player2.rect):
                print("Player 2 touched the box")
                last_box_touch_time = pygame.time.get_ticks()
                box = None
                            
            if last_box_touch_time is not None and pygame.time.get_ticks() - last_box_touch_time >= 20000:  # Đợi 10 giây trước khi tạo hộp mới
                # Tính toán vị trí mới của hộp dựa trên số giờ và số phút hiện tại
                new_box_x = (player.rect.x + player2.rect.x) / 2 # Tính toán vị trí x mới
                new_box_y = (player.rect.y + player2.rect.y) / 2  
                box = map.Box(new_box_x, new_box_y, 45)
                last_box_touch_time = pygame.time.get_ticks()
           
            if count == 2:
                draw(window, background, bg_image, player, player2, floor, fruits,fruit_opponent,box, input_text, input_visible,scroll_offset,fruits2)



            
            if initial_player1_lives <= 0:
                pygame.mixer.music.stop()
                lose.main_menu("LOSE",player.name,chosen_character)
                initial_player1_lives = lives
                initial_player2_lives = lives
            elif initial_player2_lives <= 0:
                pygame.mixer.music.stop()
                win.main_menu("WIN",player.name,chosen_character)
                initial_player1_lives = lives
                initial_player2_lives = lives
                
            # print("Player's position:", player.rect.x, player.rect.y)
            # print("name_character",chosen_character)
            # print("name", name)
            # print("name_fruit",item.name_fruit)
        pygame.quit()
        quit()
    finally:
        close_connection()  # Đóng kết nối khi chương trình kết thúc


if __name__ == "__main__":
    main(window, "abc", "bbb",10)
    