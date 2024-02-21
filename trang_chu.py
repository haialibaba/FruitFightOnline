import pygame
import sys
import main
import option_page
pygame.init()

# Thiết lập cửa sổ game
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 640
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fruit Fight")
font_path = "assets/font/anta.ttf"
# Load hình ảnh nền
background_image = pygame.image.load("assets/Background/trang_chu.jpg")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Font
font = pygame.font.Font(None, 36)
font_trangchu = pygame.font.Font(font_path, 80)

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

def main_menu():
    while True:
        screen.blit(background_image, (0, 0))  # Chèn hình ảnh nền vào cửa sổ trò chơi

        draw_text("Fruit Fight Online", font_trangchu, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
        button_width = 200  # Độ rộng của nút
        button_height = 50  # Độ cao của nút
        button_radius = 30  # Bán kính của góc bo tròn

        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Kiểm tra nếu con trỏ chuột nằm trên nút "Start"
        start_hovered = (SCREEN_WIDTH // 2 - button_width // 2 <= mouse_x <= SCREEN_WIDTH // 2 + button_width // 2 and
                         SCREEN_HEIGHT // 2 - button_height // 2 <= mouse_y <= SCREEN_HEIGHT // 2 + button_height // 2)
        
        # Kiểm tra nếu con trỏ chuột nằm trên nút "About"
        about_hovered = (SCREEN_WIDTH // 2 - button_width // 2 <= mouse_x <= SCREEN_WIDTH // 2 + button_width // 2 and
                         (SCREEN_HEIGHT // 2 + 100) - button_height // 2 <= mouse_y <= (SCREEN_HEIGHT // 2 + 100) + button_height // 2)
        
        # Kiểm tra nếu con trỏ chuột nằm trên nút "Custom"
        custom_hovered = (SCREEN_WIDTH // 2 - button_width // 2 <= mouse_x <= SCREEN_WIDTH // 2 + button_width // 2 and
                          (SCREEN_HEIGHT // 2 + 200) - button_height // 2 <= mouse_y <= (SCREEN_HEIGHT // 2 + 200) + button_height // 2)

        draw_button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, button_width, button_height, BLACK, button_radius, start_hovered)
        draw_text("Start", font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        draw_button(SCREEN_WIDTH // 2,  (SCREEN_HEIGHT // 2) + 100, button_width, button_height, BLACK, button_radius, about_hovered)
        draw_text("Options", font, WHITE, SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) + 100)

        draw_button(SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) + 200, button_width, button_height, BLACK, button_radius, custom_hovered)
        draw_text("Custom", font, WHITE, SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) + 200)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Kiểm tra nếu là sự kiện nhấn chuột trái
                    mouse_x, mouse_y = event.pos
                    # Kiểm tra nếu con trỏ chuột nằm trên nút "Start"
                    if (SCREEN_WIDTH // 2 - button_width // 2 <= mouse_x <= SCREEN_WIDTH // 2 + button_width // 2 and
                        SCREEN_HEIGHT // 2 - button_height // 2 <= mouse_y <= SCREEN_HEIGHT // 2 + button_height // 2):
                        main.main(screen)
                    elif (SCREEN_WIDTH // 2 - button_width // 2 <= mouse_x <= SCREEN_WIDTH // 2 + button_width // 2 and
                          (SCREEN_HEIGHT // 2 + 100) - button_height // 2 <= mouse_y <= (SCREEN_HEIGHT // 2 + 100) + button_height // 2):
                        option_page.main_menu()
           
if __name__ == "__main__":
    main_menu()
    # Đoạn mã chạy trò chơi sẽ ở đây khi người chơi bắt đầu từ trang chủ
