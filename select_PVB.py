import pygame
import sys
import os
import random
import math
import trang_chu
import pygame
from os import listdir
from os.path import isfile, join
import item
import player_offline
import main_vsBot
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
back_img = pygame.image.load("assets/Other/back.png")  # Điều chỉnh đường dẫn của tệp ảnh
background_image = pygame.image.load("assets/Background/choose_player.jpg")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.Font(font_path, 36)
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

        # Trả về biến cờ để kiểm soát trong hàm main_menu()
        yield False


def draw_button_with_image(image_path, x, y, width, height, hovered=False):
    button_image = pygame.image.load(image_path)
    button_image = pygame.transform.scale(button_image, (width, height))
    button_rect = button_image.get_rect(center=(x, y))
    if hovered:
        button_image.set_alpha(150)  # Giảm độ trong suốt khi hover
    screen.blit(button_image, button_rect)
    return  button_rect  # Trả về cả button_image và button_rect

def draw_button_with_image(image_path, x, y, width, height, hovered=False):
    button_image = pygame.image.load(image_path)
    button_image = pygame.transform.scale(button_image, (width, height))
    button_rect = button_image.get_rect(center=(x, y))
    if hovered:
        button_image.set_alpha(150)  # Giảm độ trong suốt khi hover
    else:
        button_image.set_alpha(255)  # Đặt lại độ trong suốt khi không hover
    screen.blit(button_image, button_rect)
    return button_rect


def info_player(chosen_character):
    character_info = {
        "MaskDude": {
            "name": "MaskDude",
            "description": "As the leader of a tribe hidden deep in the Amazon forest, he has fast movement speed and good accuracy, but in return his jumping ability is not very good."
        },
        "NinjaFrog": {
            "name": "NinjaFrog",
            "description": "NinjaFrog is a skilled ninja, moving quickly and silently. His agility and ability to jump very high make him a formidable opponent but he throws quite slowly due to his severe nearsightedness."
        },
        "PinkMan": {
            "name": "PinkMan",
            "description": "PinkMan is a mysterious character with incredible strength and resilience. He can throw fruit at a very fast speed and jump very high instead he is very slow."
        },
        "VirtualGuy": {
            "name": "VirtualGuy",
            "description": "VirtualGuy is a digital warrior with unparalleled computing power. He is very good at analysis and strategizing. His strengths are jumping high and running very fast"
        }
    }

    draw_button(730, 190, 300, 60, WHITE, 10)
    draw_button(730, 350, 400, 220, WHITE, 10)
    
    # Kiểm tra xem nhân vật đã được chọn có trong từ điển thông tin không
    if chosen_character in character_info:
        character_name = character_info[chosen_character]["name"]
        character_description = character_info[chosen_character]["description"]
        draw_text(character_name, font_charactername, GRAY, 735, 260)
        draw_text_multiline(character_description, font_charactername, BLACK, 730, 330, 380)

character_paths = {
    "MaskDude": "assets/MainCharacters/MaskDude/run.png",
    "NinjaFrog": "assets/MainCharacters/NinjaFrog/run.png",
    "PinkMan": "assets/MainCharacters/PinkMan/run.png",
    "VirtualGuy": "assets/MainCharacters/VirtualGuy/run.png"
}

character_stats = {
    "MaskDude": {"velocity": 6, "throw_speed": 1300,"jump_high": 4},
    "NinjaFrog": {"velocity": 8, "throw_speed": 1500,"jump_high": 7},
    "PinkMan": {"velocity": 4, "throw_speed": 1000,"jump_high":6.3},
    "VirtualGuy": {"velocity": 6.5, "throw_speed": 1300,"jump_high":6},
}

def main_menu():
    chosen_character = None
    input_text = ''
    running = True
    clock = pygame.time.Clock()

    frame_index = 0  # Biến để theo dõi khung hình hiện tại của hoạt ảnh
    animation_speed = 0.1  # Tốc độ chuyển đổi giữa các khung hình
    last_frame_update = pygame.time.get_ticks()  # Thời điểm cuối cùng cập nhật khung hình

    while running:
        button_clicked = False
        screen.blit(background_image, (0, 0))
        draw_button(500, 320, 900, 500, LIGHTSKYBLUE, 10)
        draw_text("Fruit Fight Online PVB", font, BLACK, 250, 120)
        draw_button(250, 350, 300, 380, YELLOW, 10)

        button_rect1 = draw_button_with_image("assets/Background/button.png", 145, 200, 60, 60)
        button_rect2 = draw_button_with_image("assets/Background/button.png", 215, 200, 60, 60)
        button_rect3 = draw_button_with_image("assets/Background/button.png", 285, 200, 60, 60)
        button_rect4 = draw_button_with_image("assets/Background/button.png", 355, 200, 60, 60)

        info_player(chosen_character)

        draw_button_start(SCREEN_WIDTH - 200 // 2 - 120, SCREEN_HEIGHT - 50 // 2 - 90, 200, 50, WHITE, 10)
        draw_text("Start", font, BLACK, SCREEN_WIDTH - 200 // 2 - 120, SCREEN_HEIGHT - 50 // 2 - 90)
        

        # Vẽ nhân vật được chọn
        if chosen_character:
            player_offline.Player.SPRITES = player_offline.load_sprite_sheet("MainCharacters", chosen_character, 32, 32, True)
            main_vsBot.Player_VEL_1 = character_stats[chosen_character]["velocity"]
            main_vsBot.speed_throw_1 = character_stats[chosen_character]["throw_speed"]
            player_offline.Player_jump = character_stats[chosen_character]["jump_high"]
            character_frames = load_animation_frames(chosen_character, 32, 32)
            if character_frames:
                current_time = pygame.time.get_ticks()
                if current_time - last_frame_update >= animation_speed * 1000:
                    frame_index += 1
                    last_frame_update = current_time

                frame_index %= len(character_frames)  # Đảm bảo frame_index không vượt quá số lượng khung hình
                current_frame = character_frames[frame_index]
                screen.blit(current_frame, (175, 310))
        else:
            character_frames = load_animation_frames("MaskDude", 32, 32)
            info_player("MaskDude")
            if character_frames:
                current_time = pygame.time.get_ticks()
                if current_time - last_frame_update >= animation_speed * 1000:
                    frame_index += 1
                    last_frame_update = current_time

                frame_index %= len(character_frames)  # Đảm bảo frame_index không vượt quá số lượng khung hình
                current_frame = character_frames[frame_index]
                screen.blit(current_frame, (175, 310))

        draw_text("NAME: ", font_name, BLACK, 650, 190)
        draw_input_box(698, 161, 160, 40, input_text)
        screen.blit(back_img, (20, 16))
        clock.tick(FPS)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = event.pos
                    if button_rect1.collidepoint(mouse_pos):
                        chosen_character = "MaskDude"
                        button_clicked = True
                    elif button_rect2.collidepoint(mouse_pos):
                        chosen_character = "NinjaFrog"
                        button_clicked = True
                    elif button_rect3.collidepoint(mouse_pos):
                        chosen_character = "PinkMan"
                        button_clicked = True
                    elif button_rect4.collidepoint(mouse_pos):
                        chosen_character = "VirtualGuy"
                        button_clicked = True
                    elif 700 <= mouse_pos[0] <= 700 + 170 and \
                    500 <= mouse_pos[1] <= 500 + 50:
                        if not input_text.strip():
                            input_text = "Player"
                        main_vsBot.main(screen,chosen_character,"NinjaFrog",input_text,"BOT",15)
                    elif 20 <= mouse_pos[0] <= 20 + 50 and \
                    16 <= mouse_pos[1] <= 16 + 50:
                        trang_chu.main_menu()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_RETURN:
                    print("Entered text:", input_text)
                elif len(input_text) < 7:
                    input_text += event.unicode

        pygame.display.flip()
        
        if button_clicked:
            pygame.display.update()

if __name__ == "__main__":
    main_menu()