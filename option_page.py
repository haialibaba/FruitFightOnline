import pygame
import sys
import main

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 640
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fruit Fight")
font_path = "assets/font/anta.ttf"

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)

background_image = pygame.image.load("assets/Background/trang_chu.jpg")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

apple_img = pygame.image.load("assets/about_picture/apple.png")
apple_img = pygame.transform.scale(apple_img, (60, 60))

banana_img = pygame.image.load("assets/about_picture/banana.png")
banana_img = pygame.transform.scale(banana_img, (50, 50))

cherry_img = pygame.image.load("assets/about_picture/cherry.png")
cherry_img = pygame.transform.scale(cherry_img, (50, 50))

pineapple_img = pygame.image.load("assets/about_picture/pineapple.png")
pineapple_img = pygame.transform.scale(pineapple_img, (50, 50))

melon_img = pygame.image.load("assets/about_picture/watermelon.png")
melon_img = pygame.transform.scale(melon_img, (60, 60))

kiwi_img = pygame.image.load("assets/about_picture/kiwi.png")
kiwi_img = pygame.transform.scale(kiwi_img, (50, 50))

lemon_img = pygame.image.load("assets/about_picture/lemon.png")
lemon_img = pygame.transform.scale(lemon_img, (45, 45))

strawberry_img = pygame.image.load("assets/about_picture/strawberry.png")
strawberry_img = pygame.transform.scale(strawberry_img, (60, 60))

font = pygame.font.Font(None, 36)
font_trangchu = pygame.font.Font(font_path, 80)
font_about_fruit = pygame.font.Font(font_path, 18)

def draw_text(text, font, color, x, y, bold=True):
    text_surface = font.render(text, bold, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def draw_arrow_icon_up(x, y, size):
    pygame.draw.polygon(screen, BLACK, [(x + size//2, y), (x + size, y + size), (x, y + size)])

def draw_arrow_icon_left(x, y, size):
    pygame.draw.polygon(screen, BLACK, [(x + size, y), (x, y + size//2), (x + size, y + size)])

def draw_arrow_icon_right(x, y, size):
    pygame.draw.polygon(screen, BLACK, [(x, y), (x + size, y + size//2), (x, y + size), (x, y)])

def draw_rounded_rect(surface, color, rect, radius, border=0):
    x, y, width, height = rect
    pygame.draw.rect(surface, color, rect, border, border_radius=radius)

def draw_button(x, y, width, height, color, radius, hovered=False):
    rect = pygame.Rect(x - width // 2, y - height // 2, width, height)
    hover_color = (192, 192, 192)  # Xám
    if hovered:
        color = hover_color  # Thay đổi màu sắc khi hover
    draw_rounded_rect(screen, color, rect, radius)

def draw_control_area():
    font_button_arrow = pygame.font.Font(None, 28)
    button_width = 200
    button_height = 50
    button_radius = 10
    
    # Vẽ nút How To Play
    draw_button(button_width // 2 + 40, button_height // 2 + 80, 200, 50, WHITE, 10)
    draw_text("How To Play", font, BLACK, button_width // 2 + 40, button_height // 2 + 80)
    
    draw_button(button_width // 2 + 40, button_height // 2 + 330, 200, 400, WHITE, 10)

    # Vẽ mũi tên hướng lên trên
    draw_text("Up", font_button_arrow, BLACK, button_width // 2 + 40, button_height // 2 + 180)
    draw_button(button_width // 2 + 40, button_height // 2 + 217, 45, 45, GRAY, 10)
    draw_arrow_icon_up(button_width // 2 + 25, button_height // 2 + 200, 30)
    
    # Vẽ mũi tên hướng qua trái
    draw_text("Left", font_button_arrow, BLACK, button_width // 2 - 23, button_height // 2 + 250)
    draw_button(button_width // 2 - 23, button_height // 2 + 285, 45, 45, GRAY, 10)
    draw_arrow_icon_left(button_width // 2 - 40, button_height // 2 + 270, 30)

    # Vẽ mũi tên hướng qua phải
    draw_text("Right", font_button_arrow, BLACK, button_width // 2 + 103, button_height // 2 + 250)
    draw_button(button_width // 2 + 103, button_height // 2 + 285, 45, 45, GRAY, 10)
    draw_arrow_icon_right(button_width // 2 + 90, button_height // 2 + 270, 30)

    # Vẽ nút space
    draw_button(button_width // 2 + 40, button_height // 2 + 365, 150, 45, GRAY, 10)
    draw_text("Space", font_button_arrow, BLACK, button_width // 2 + 40, button_height // 2 + 365)
    draw_text("Shooting", font_button_arrow, BLACK, button_width // 2 + 40, button_height // 2 + 410)

def draw_about_fruit():
    font_button_arrow = pygame.font.Font(None, 28)
    button_width = 200
    button_height = 50
    button_radius = 10
    
    # Vẽ nút About fruit
    draw_button(button_width // 2 + 520, button_height // 2 + 80, 700, 50, WHITE, 10)
    draw_text("About Fruit", font, BLACK, button_width // 2 + 540, button_height // 2 + 80)
    
    #wap fruit
    draw_button(button_width // 2 + 520, button_height // 2 + 330, 700, 400, WHITE, 10)

    #apple
    draw_text("Base speed and damage", font_about_fruit, BLACK, button_width // 2 + 330, button_height // 2 + 170)
    screen.blit(apple_img, (button_width // 2 + 175, button_height // 2 + 140)) 

    #Banana
    draw_text("High speed and base damage", font_about_fruit, BLACK, button_width // 2 + 730, button_height // 2 + 170)
    screen.blit(banana_img, (button_width // 2 + 540, button_height // 2 + 140))

    #Cherry
    draw_text("Very high speed but low damage", font_about_fruit, BLACK, button_width // 2 + 370, button_height // 2 + 270)
    screen.blit(cherry_img, (button_width // 2 + 183, button_height // 2 + 240))

    #Pineapple
    draw_text("High speed and high damage", font_about_fruit, BLACK, button_width // 2 + 730, button_height // 2 + 270)
    screen.blit(pineapple_img, (button_width // 2 + 550, button_height // 2 + 240))

    #watermelon
    draw_text("Low speed but very high damage", font_about_fruit, BLACK, button_width // 2 + 370, button_height // 2 + 370)
    screen.blit(melon_img, (button_width // 2 + 173, button_height // 2 + 340))

    #Kiwi
    draw_text("High speed but base damage", font_about_fruit, BLACK, button_width // 2 + 730, button_height // 2 + 370)
    screen.blit(kiwi_img, (button_width // 2 + 553, button_height // 2 + 346))

    #lemon
    draw_text("Very High speed but base damage", font_about_fruit, BLACK, button_width // 2 + 370, button_height // 2 + 470)
    screen.blit(lemon_img, (button_width // 2 + 173, button_height // 2 + 440))

    #strawberry
    draw_text("High speed and damage", font_about_fruit, BLACK, button_width // 2 + 730, button_height // 2 + 470)
    screen.blit(strawberry_img, (button_width // 2 + 553, button_height // 2 + 440))

def draw_button_back(x, y, width, height, color, radius, hovered=False):
    rect = pygame.Rect(x - width // 2, y - height // 2, width, height)
    hover_color = (192, 192, 192)  # Màu xám khi hover

    # Kiểm tra xem chuột có hover vào nút hay không
    mouse_x, mouse_y = pygame.mouse.get_pos()
    is_hovered = rect.collidepoint(mouse_x, mouse_y)

    if is_hovered:
        color = hover_color  # Thay đổi màu sắc khi hover

    draw_rounded_rect(screen, color, rect, radius)

def main_menu():
    while True:
        screen.blit(background_image, (0, 0))
        
        button_width = 200
        button_height = 50
        button_radius = 10

        # Vẽ nút About Fruit ở góc phải dưới cuối màn hình
        draw_button_back(SCREEN_WIDTH - button_width // 2 - 20, SCREEN_HEIGHT - button_height // 2 - 20, 200, 50, WHITE, 10)
        draw_text("Back", font, BLACK, SCREEN_WIDTH - button_width // 2 - 20, SCREEN_HEIGHT - button_height // 2 - 20)

        draw_control_area()
        draw_about_fruit()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Kiểm tra nếu là sự kiện nhấn chuột trái
                    mouse_x, mouse_y = event.pos
                    # Kiểm tra nếu con trỏ chuột nằm trên nút "Back"
                    if (SCREEN_WIDTH - button_width // 2 - 20 - button_width // 2 <= mouse_x <= SCREEN_WIDTH - button_width // 2 - 20 + button_width // 2 and
                        SCREEN_HEIGHT - button_height // 2 - 20 - button_height // 2 <= mouse_y <= SCREEN_HEIGHT - button_height // 2 - 20 + button_height // 2):
                        return

if __name__ == "__main__":
    main_menu()
