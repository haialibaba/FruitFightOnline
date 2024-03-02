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
pygame.display.set_caption('Client')

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_host = '192.168.43.154'
server_port = 8080

client_socket.connect((server_host, server_port))

print("Connected to server.")

def send_coordinate():
    # Hàm này được chạy trong một luồng riêng biệt để gửi tọa độ của người chơi lên server liên tục
    while True:
        data = f"COORD:{player_x} {player_y}"
        client_socket.send(data.encode())
        pygame.time.delay(50)

def send_chat_message(message):
    # Hàm này được gọi khi muốn gửi một tin nhắn chat lên server
    data = f"CHAT:{message}"
    client_socket.send(data.encode())

def receive_data():
    # Hàm này nhận dữ liệu từ server và xác định loại dữ liệu (tọa độ hoặc tin nhắn chat)
    data = client_socket.recv(1024).decode()
    if data.startswith("COORD:"):
        try:
            x, y = map(int, data[6:].split())
            return x, y
        except ValueError:
            return 0, 0
    elif data.startswith("CHAT:"):
        return data[5:], "CHAT"  # Trả về tin nhắn và đánh dấu loại dữ liệu là "CHAT"
    return 0, 0

player_x = 50
player_y = 50
speed = 5
fall_speed = 0
jump_height = 100
jumping = False

chat_font = pygame.font.Font(None, 24)
input_rect = pygame.Rect(10, WINDOW_HEIGHT - 30, 300, 20)
chat_text = ''
chat_history = []
typing = False  # Trạng thái đánh máy: True nếu đang nhập tin nhắn, False nếu không

send_thread = threading.Thread(target=send_coordinate)
send_thread.start()  # Khởi động luồng gửi tọa độ

running = True
while running:
    window.fill(WHITE)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_UP and not jumping:
                jumping = True
            elif event.key == K_RETURN:
                if not typing:
                    typing = True  # Kích hoạt trạng thái nhập tin nhắn
                else:
                    # Gửi tin nhắn khi nhấn Enter lần thứ hai
                    send_chat_message(chat_text)
                    chat_history.append("ME: " + chat_text)
                    chat_text = ''
                    typing = False  # Tắt trạng thái nhập tin nhắn sau khi đã gửi
            elif event.key == K_BACKSPACE:
                chat_text = chat_text[:-1]
            elif typing and event.key != K_RETURN:
                chat_text += event.unicode  # Thêm ký tự vào tin nhắn nếu đang nhập

    other_player_x, other_player_y = receive_data()
    if other_player_y == "CHAT":
        chat_history.append("USER: "+ other_player_x)  # Hiển thị tin nhắn chat từ người chơi khác
    else:
        pygame.draw.rect(window, RED, (other_player_x, other_player_y, 50, 50))

    keys = pygame.key.get_pressed()
    if keys[K_LEFT]:
        player_x -= speed
    if keys[K_RIGHT]:
        player_x += speed

    if jumping:
        player_y -= speed
        if player_y <= other_player_y - jump_height:
            jumping = False
    else:
        player_y += fall_speed
        fall_speed += 1

    if player_y >= WINDOW_HEIGHT - 50:
        player_y = WINDOW_HEIGHT - 50
        fall_speed = 0

    player_x = max(0, min(player_x, WINDOW_WIDTH - 50))
    player_y = max(0, min(player_y, WINDOW_HEIGHT - 50))

    pygame.draw.rect(window, RED, (player_x, player_y, 50, 50))

    for i, message in enumerate(chat_history):
        text_surface = chat_font.render(message, True, (0, 0, 0))
        window.blit(text_surface, (10, i * 20))

    pygame.draw.rect(window, (0, 0, 0), input_rect, 2)
    if typing:
        pygame.draw.rect(window, (200, 200, 200), input_rect)  # Vùng nhập tin nhắn
        text_surface = chat_font.render(chat_text, True, (0, 0, 0))
        window.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
    else:
        pygame.draw.rect(window, (200, 200, 200), input_rect, 2)  # Khung nhập tin nhắn

    pygame.display.update()

client_socket.close()