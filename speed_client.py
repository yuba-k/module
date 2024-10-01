import socket
import numpy as np
import cv2

# ソケットの設定
socket_path = '/tmp/ram/camera.sock'

def receive_images():
    # ソケットの作成
    client_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client_socket.connect(socket_path)

    try:
        while True:
            # データを受信
            data = bytearray()
            while True:
                # 受信データを逐次追加
                packet = client_socket.recv(4096)
                if not packet:
                    break
                data.extend(packet)

            # 受信したデータから画像をデコード
            img_array = np.frombuffer(data, np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

            if img is not None:
                cv2.imshow('Received Image', img)  # 画像を表示
                cv2.waitKey(1)  # 表示を更新

    finally:
        client_socket.close()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    receive_images()
