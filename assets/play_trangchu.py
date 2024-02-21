import pygame
import sys

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

def main_menu():
    while True:
        screen.blit(background_image, (0, 0))

        draw_button(500, 320, 900, 500, LIGHTSKYBLUE, 10)

        draw_text("Fruit Fight Online", font, BLACK, 250, 120)

        draw_button(250, 350, 300, 380, YELLOW, 10)

        draw_button(145, 200, 60, 30, GRAY, 10)

        draw_button(215, 200, 60, 30, GRAY, 10)

        draw_button(285, 200, 60, 30, GRAY, 10)

        draw_button(355, 200, 60, 30, GRAY, 10)


        draw_button(730, 190, 300, 60, YELLOW, 10)

        draw_button(730, 350, 300, 220, YELLOW, 10)

        draw_button_start(SCREEN_WIDTH - 200 // 2 - 120, SCREEN_HEIGHT - 50 // 2 - 90, 200, 50, WHITE, 10)
        draw_text("Start", font, BLACK, SCREEN_WIDTH - 200 // 2 - 120, SCREEN_HEIGHT - 50 // 2 - 90)
        
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    main_menu()