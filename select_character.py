import pygame
import sys
import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join
import item
import character
pygame.init()

FPS = 60
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 640
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fruit Fight")
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



def draw_text(text, font, color, x, y, bold=True):
    text_surface = font.render(text, bold, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def draw_rounded_rect(surface, color, rect, radius, border=0):
    x, y, width, height = rect
    pygame.draw.rect(surface, color, rect, border, border_radius=radius)

def draw_button(x, y, width, height, color, radius, hovered=False):
    rect = pygame.Rect(x - width // 2, y - height // 2, width, height)
    hover_color = (192, 192, 192)  # Xám
    if hovered:
        color = hover_color  # Thay đổi màu sắc khi hover
    draw_rounded_rect(screen, color, rect, radius)

def draw_button_player(x, y, width, height, color, radius_left, radius_right, hovered=False):
    rect = pygame.Rect(x - width // 2, y - height // 2, width, height)
    hover_color = (192, 192, 192)  # Xám
    if hovered:
        color = hover_color  # Thay đổi màu sắc khi hover

    # Vẽ phần bên trái của nút với bán kính cong
    left_rect = pygame.Rect(rect.left, rect.top, width // 2, height)
    pygame.draw.rect(screen, color, left_rect, border_radius=(radius_left, 0, 0, radius_left))

    # Vẽ phần bên phải của nút với bán kính cong
    right_rect = pygame.Rect(rect.left + width // 2, rect.top, width // 2, height)
    pygame.draw.rect(screen, color, right_rect, border_radius=(0, radius_right, radius_right, 0))

    # Vẽ bánh xe bên trái của nút
    pygame.draw.circle(screen, color, (rect.left + radius_left, rect.top + radius_left), radius_left)

    # Vẽ bánh xe bên phải của nút (chỉ vẽ khi đang hover)
    if hovered:
        pygame.draw.circle(screen, color, (rect.right - radius_right, rect.top + radius_right), radius_right)

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
    running = True

    while running:
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
                running = False
                break

    # Kết thúc vòng lặp, trả về biến running để có thể kiểm soát ở phía main_menu()
    return running


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


def info_player():
    draw_button(730, 190, 300, 60, YELLOW, 10)
    draw_button(730, 350, 300, 220, YELLOW, 10)

character_paths = {
    "MaskDude": "assets/MainCharacters/MaskDude/run.png",
    "NinjaFrog": "assets/MainCharacters/NinjaFrog/run.png",
    "PinkMan": "assets/MainCharacters/PinkMan/run.png",
    "VirtualGuy": "assets/MainCharacters/VirtualGuy/run.png"
}
def main_menu():
    chosen_character = None
    running = True
    button_clicked = False  # Biến cờ để chỉ ra liệu có nút nào được click hay không

    while running:
        clock = pygame.time.Clock()
        screen.blit(background_image, (0, 0))

        draw_button(500, 320, 900, 500, LIGHTSKYBLUE, 10)
        draw_text("Fruit Fight Online", font, BLACK, 250, 120)
        draw_button(250, 350, 300, 380, YELLOW, 10)

        button_rect1 = draw_button_with_image("assets/Background/button.png", 145, 200, 60, 60)
        button_rect2 = draw_button_with_image("assets/Background/button.png", 215, 200, 60, 60)
        button_rect3 = draw_button_with_image("assets/Background/button.png", 285, 200, 60, 60)
        button_rect4 = draw_button_with_image("assets/Background/button.png", 355, 200, 60, 60)

        info_player()

        draw_button_start(SCREEN_WIDTH - 200 // 2 - 120, SCREEN_HEIGHT - 50 // 2 - 90, 200, 50, WHITE, 10)
        draw_text("Start", font, BLACK, SCREEN_WIDTH - 200 // 2 - 120, SCREEN_HEIGHT - 50 // 2 - 90)

        clock.tick(FPS)
        
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
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

        # Kiểm tra nếu có nút nào được click, thì cập nhật hoạt cảnh của nhân vật mới
        if button_clicked:
            character_frames = load_animation_frames(chosen_character, 32, 32)
            if character_frames:
                running = draw_character_animation(character_frames, (175, 310))
                if not running:
                    break

        button_clicked = False  # Đặt lại biến cờ
        print("Before:", button_clicked)
        button_clicked = False
        print("After:", button_clicked)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main_menu()

