import socket
import pygame
from pygame.locals import *
import threading

pygame.init()

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400

WHITE = (255, 255, 255)
RED = (255, 0, 0)

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Client 1')

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_host = socket.gethostbyname(socket.gethostname())
server_port = 12345

client_socket.connect((server_host, server_port))

print("Kết nối đến máy chủ thành công.")

# Hàm gửi tọa độ x và y từ client đến server
def send_coordinate():
    while True:
        data = f"{player_x} {player_y}"
        client_socket.send(data.encode())
        pygame.time.delay(50)  # Delay để hạn chế tốc độ gửi

# Hàm nhận dữ liệu từ server và cập nhật vị trí hình vuông của người chơi khác
def receive_data():
    while True:
        data = client_socket.recv(1024).decode()
        if data:
            try:
                x, y = map(int, data.split())
                return x, y
            except ValueError:
                return 0, 0
        else:
            return 0, 0

player_x = 50
player_y = 50
speed = 5
fall_speed = 0  # Tốc độ rơi ban đầu
jump_height = 100  # Chiều cao nhảy
jumping = False

send_thread = threading.Thread(target=send_coordinate)
receive_thread = threading.Thread(target=receive_data)

send_thread.start()
receive_thread.start()

running = True
while running:
    window.fill(WHITE)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:  # Kiểm tra khi phím được nhấn
            if event.key == K_UP and not jumping:  # Nếu là phím UP và không đang nhảy
                jumping = True  # Bắt đầu nhảy

    other_player_x, other_player_y = receive_data()

    pygame.draw.rect(window, RED, (other_player_x, other_player_y, 50, 50))

    keys = pygame.key.get_pressed()
    if keys[K_LEFT]:
        player_x -= speed
    if keys[K_RIGHT]:
        player_x += speed
    
    # Nếu đang nhảy, điều chỉnh vị trí y của người chơi
    if jumping:
        player_y -= speed  # Điều chỉnh vị trí y lên trên
        if player_y <= other_player_y - jump_height:  # Khi đạt đến chiều cao nhảy
            jumping = False  # Kết thúc nhảy
    else:
        # Nếu không nhảy, cộng thêm tốc độ rơi vào vị trí y
        player_y += fall_speed
        fall_speed += 1  # Tăng tốc độ rơi dần khi nhân vật đang rơi

    # Giới hạn vị trí y để không vượt quá biên dưới cửa sổ
    if player_y >= WINDOW_HEIGHT - 50:
        player_y = WINDOW_HEIGHT - 50
        fall_speed = 0  # Reset tốc độ rơi khi chạm đất

    player_x = max(0, min(player_x, WINDOW_WIDTH - 50))
    player_y = max(0, min(player_y, WINDOW_HEIGHT - 50))
    pygame.draw.rect(window, RED, (player_x, player_y, 50, 50))

    pygame.display.update()

client_socket.close()