import pygame
import sys
import os
import random
import math
import main
import pygame
from os import listdir
from os.path import isfile, join
import trang_chu
import subprocess
import threading
import time
pygame.init()

FPS = 60
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 640
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fruit Fight1")
font_path = "assets/font/anta.ttf"
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 60)
LIGHTSKYBLUE = (135, 206, 250)

background_image = pygame.image.load("assets/Background/choose_player.jpg")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.Font(font_path, 36)
font_win = pygame.font.Font(font_path, 70)
font_name = pygame.font.Font(font_path, 28)
font_charactername = pygame.font.Font(font_path, 18)

def draw_input_box(x, y, width, height, text=''):
    pygame.draw.rect(screen, WHITE, (x, y, width, height), 2)
    input_text = font.render(text, True, BLACK)
    screen.blit(input_text, (x + 5, y + 5))

def draw_text(text, font, color, x, y, bold=True):
    text_surface = font.render(text, bold, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)
    
def draw_text_Win_Lose(text, font, color, x, y, bold=True, delay_ms=150):
    total_width = sum(font.size(char)[0] for char in text)
    spacing = (font.size(' ')[0]) * (len(text) - 1)
    start_x = x - total_width / 2 - spacing 
    
    # Lấy thời gian bắt đầu vẽ chữ
    start_time = pygame.time.get_ticks()
    
    # Số lượng ký tự đã vẽ
    char_index = 0
    while char_index < len(text):
        # Lấy thời gian hiện tại
        current_time = pygame.time.get_ticks()
        
        # Tính thời gian đã trôi qua kể từ khi bắt đầu vẽ chữ
        elapsed_time = current_time - start_time
        
        # Nếu thời gian đã trôi qua đủ lớn so với thời gian cần chờ giữa các ký tự
        if elapsed_time >= char_index * delay_ms:
            char = text[char_index]
            char_surface = font.render(char, bold, color)
            char_rect = char_surface.get_rect()
            char_rect.topleft = (start_x, y)
            screen.blit(char_surface, char_rect)
            pygame.display.update()
            
            # Tăng chỉ số ký tự đã vẽ
            char_index += 1
            
            # Di chuyển vị trí bắt đầu vẽ cho ký tự tiếp theo
            start_x += char_rect.width + (font.size(' ')[0]) 



def draw_text_multiline(text, font, color, x, y, max_width, bold=True, line_spacing=0):
    lines = []
    words = text.split(' ')
    current_line = ''
    max_line_height = 0  # Biến để lưu trữ chiều cao lớn nhất của dòng
    for word in words:
        test_line = current_line + word + ' '
        test_rect = font.render(test_line, bold, color).get_rect()
        if test_rect.width > max_width:
            lines.append(current_line.strip())
            max_line_height = max(max_line_height, font.size(current_line.strip())[1])  # Cập nhật chiều cao lớn nhất
            current_line = word + ' '
        else:
            current_line = test_line
    lines.append(current_line.strip())
    max_line_height = max(max_line_height, font.size(current_line.strip())[1])  # Cập nhật chiều cao lớn nhất

    total_height = len(lines) * max_line_height  # Tính toán chiều cao tổng cộng của văn bản
    # Y position for the first line
    current_y = y - total_height // 2
    for line in lines:
        text_surface = font.render(line, bold, color)
        text_rect = text_surface.get_rect()
        text_rect.centerx = x
        text_rect.y = current_y
        screen.blit(text_surface, text_rect)
        # Move to the next line position
        current_y += max_line_height + line_spacing


def draw_rounded_rect(surface, color, rect, radius, border=0):
    x, y, width, height = rect
    pygame.draw.rect(surface, color, rect, border, border_radius=radius)

def draw_button(x, y, width, height, color, radius, hovered=False):
    rect = pygame.Rect(x - width // 2, y - height // 2, width, height)
    hover_color = (192, 192, 192)  # Xám
    if hovered:
        color = hover_color  # Thay đổi màu sắc khi hover
    draw_rounded_rect(screen, color, rect, radius)

def draw_button_player(x, y, width, height, color, radius_left, radius_right):
    rect = pygame.Rect(x - width // 2, y - height // 2, width, height)
    # Vẽ phần bên trái của nút với bán kính cong
    left_rect = pygame.Rect(rect.left, rect.top, width // 2, height)
    pygame.draw.rect(screen, color, left_rect, border_radius=(radius_left, 0, 0, radius_left))

    # Vẽ phần bên phải của nút với bán kính cong
    right_rect = pygame.Rect(rect.left + width // 2, rect.top, width // 2, height)
    pygame.draw.rect(screen, color, right_rect, border_radius=(0, radius_right, radius_right, 0))

    # Vẽ bánh xe bên trái của nút
    pygame.draw.circle(screen, color, (rect.left + radius_left, rect.top + radius_left), radius_left)

def draw_button_start(x, y, width, height, color, radius, hovered=False):
    rect = pygame.Rect(x - width // 2, y - height // 2, width, height)
    hover_color = (192, 192, 192)  # Màu xám khi hover

    # Kiểm tra xem chuột có hover vào nút hay không
    mouse_x, mouse_y = pygame.mouse.get_pos()
    is_hovered = rect.collidepoint(mouse_x, mouse_y)

    if is_hovered:
        color = hover_color  # Thay đổi màu sắc khi hover

    draw_rounded_rect(screen, color, rect, radius)

def load_animation_frames(character_name, frame_width, frame_height, scale=4.5):
    animation_frames = []
    if character_name in character_paths:
        image_path = character_paths[character_name]
        character_image = pygame.image.load(image_path)
        image_rect = character_image.get_rect()
        num_columns = image_rect.width // frame_width
        num_rows = image_rect.height // frame_height

        for row in range(num_rows):
            for col in range(num_columns):
                frame_rect = pygame.Rect(col * frame_width, row * frame_height, frame_width, frame_height)
                frame_surface = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
                frame_surface.blit(character_image, (0, 0), frame_rect)
                # Tăng kích thước của frame
                scaled_frame_surface = pygame.transform.scale(frame_surface, (frame_width * scale, frame_height * scale))
                animation_frames.append(scaled_frame_surface)
    else:
        print(f"Character '{character_name}' not found in character_paths dictionary.")

    return animation_frames

def draw_character_animation(frames, position):
    frame_index = 0
    animation_speed = 0.1  # Tốc độ chuyển đổi giữa các frame
    last_frame_update = pygame.time.get_ticks()

    while True:
        current_time = pygame.time.get_ticks()
        if current_time - last_frame_update >= animation_speed * 1000:
            frame_index += 1
            last_frame_update = current_time

        frame_index %= len(frames)  # Lặp lại các khung hình
        current_frame = frames[frame_index]

        screen.fill((255, 255, 60), (position[0], position[1], current_frame.get_width(), current_frame.get_height()))
        screen.blit(current_frame, position)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        yield False

character_paths = {
    "MaskDude": "assets/MainCharacters/MaskDude/run.png",
    "NinjaFrog": "assets/MainCharacters/NinjaFrog/run.png",
    "PinkMan": "assets/MainCharacters/PinkMan/run.png",
    "VirtualGuy": "assets/MainCharacters/VirtualGuy/run.png"
}

def open_new_window():
    subprocess.run(["python", "trang_chu.py"])
    main.close_connection()

def main_menu(text,name,chosen_character):
    pygame.mixer.music.stop()
    input_text = ''
    running = True
    clock = pygame.time.Clock()
    frame_index = 0  # Biến để theo dõi khung hình hiện tại của hoạt ảnh
    animation_speed = 0.1  # Tốc độ chuyển đổi giữa các khung hình
    last_frame_update = pygame.time.get_ticks()  # Thời điểm cuối cùng cập nhật khung hình
    check = False

    if text == "WIN":
        draw_text_Win_Lose("YOU WIN .....", font_win, GRAY, 660, 230)
    elif text == "LOSE":
        draw_text_Win_Lose("YOU LOSE .....", font_win, GRAY, 660, 230)

    while running:
        button_clicked = False
        screen.blit(background_image, (0, 0))
        draw_button(500, 320, 750, 450, LIGHTSKYBLUE, 10)

        draw_button_start(SCREEN_WIDTH - 200 // 2 - 70, SCREEN_HEIGHT - 50 // 2 - 30, 170, 50, WHITE, 10)
        draw_text("HOME", font, BLACK, SCREEN_WIDTH - 200 // 2 - 70, SCREEN_HEIGHT - 50 // 2 - 30)
        
        if text == "WIN":
            draw_text("CONGRATULATION WINNER", font, GRAY, 510, 160)
            if check == False:
                win_sound = pygame.mixer.Sound("assets/music/win_sound.mp3")
                win_sound.play()
                check = True
        elif text == "LOSE":
            draw_text("TRY HARDER", font, GRAY, 510, 160)
            if check == False:
                lose_sound = pygame.mixer.Sound("assets/music/lose_sound.mp3")
                lose_sound.play()  # Phát âm thanh
                check = True

           

        # Vẽ nhân vật được chọn
        draw_text(name, font, BLACK, 510, 280)
        character_frames = load_animation_frames(chosen_character, 32, 32)
        if character_frames:
            current_time = pygame.time.get_ticks()
            if current_time - last_frame_update >= animation_speed * 1000:
                frame_index += 1
                last_frame_update = current_time

            frame_index %= len(character_frames)  # Đảm bảo frame_index không vượt quá số lượng khung hình
            current_frame = character_frames[frame_index]
            screen.blit(current_frame, (430, 310))


        clock.tick(FPS)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = event.pos
                    if 750 <= mouse_pos[0] <= 750 + 150 and \
                    560 <= mouse_pos[1] <= 560 + 50:
                        threading.Thread(target=open_new_window).start()
                        time.sleep(1)
                        os._exit(0)

                        


        pygame.display.flip()
        
        if button_clicked:
            pygame.display.update()

if __name__ == "__main__":
    text = "LOSE"
    name = "kha"
    chosen_character = "MaskDude"
    main_menu(text,name,chosen_character)