import threading

map_id = None  # Khởi tạo map_id với giá trị None

def receive_thread():
    global map_id  # Sử dụng biến global map_id
    map_id = 1

# Tạo một luồng để chạy receive_thread()
receive_thread_instance = threading.Thread(target=receive_thread)
receive_thread_instance.start()

# Trong hàm main
if __name__ == "__main__":
    print(map_id)
