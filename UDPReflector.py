# Unityでは、ビルドしないと外部からの通信ができない。
# ローカルの通信はできるため、Pythonを介して外部との通信を行う。

import socket

# 受信側設定
UDP_IP = "192.168.100.54"   # 自分のIP
UDP_PORT = 8052

# 送信先設定
SEND_IP = "192.168.100.54"  # 転送先のIPアドレス
SEND_PORT = 8051             # 転送先のポート番号

# 受信用ソケットの準備
recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recv_sock.bind((UDP_IP, UDP_PORT))

# 送信用ソケットの準備
send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print(f"Listening on {UDP_IP}:{UDP_PORT}, forwarding to {SEND_IP}:{SEND_PORT}...")

# 無限ループで常に受信を待ち続ける
while True:
    try:
        data, addr = recv_sock.recvfrom(1024)
        print(f"Received from {addr}: {data.decode(errors='ignore')}")
        
        # 受信データをそのまま転送
        send_sock.sendto(data, (SEND_IP, SEND_PORT))
        print(f"Forwarded to {SEND_IP}:{SEND_PORT}")
        
    except KeyboardInterrupt:
        print("exit")
        break
    except Exception as e:
        print("error:", e)
