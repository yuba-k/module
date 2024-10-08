import socket
import numpy as np
import cv2

# ソケットの設定
ipaddr = "192.168.171.38"
port = 8000
socket_path = ((ipaddr,8000))

def receive_images():
    # ソケットの作成
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ipaddr,8000))

    try:
        i = 0
        while True:
            # データを受信
            data = bytearray()
            while True:
                try:
                    # 受信データを逐次追加
                    packet = client_socket.recv(4096)
                    if b"fin" in packet:
                        packet = packet.replace(b"fin",b"===")
                        data.extend(packet)
                        break
                    data.extend(packet)
                except Exception as e:
                    print(e)
            # 受信したデータから画像をデコード
            img_array = np.frombuffer(data, np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

            if img is not None:
                cv2.imshow('Received Image', img)  # 画像を表示
                cv2.waitKey(1)  # 表示を更新
                i += 1

    finally:
        client_socket.close()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    receive_images()