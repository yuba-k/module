import socket
import numpy as np
import cv2
import threading
import tkinter as tk

# ソケットの設定
ipaddr = "192.168.171.132"
port = 8000
socket_path = ((ipaddr,8000))

class Window():
    def __init__(self,root):
        self.root = root
        self.image_label = tk.Label(self.root)
        self.image_label.pack()

        self.running = 1

        threading.Thread(target=self.receive_images).start()

        self.update_image()

    def receive_images():
        # ソケットの作成
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ipaddr,8000))

        try:
            i = 0
            while True:
                # データを受信
                data = bytearray()
                while self.running:
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
                self.img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

                if img is not None:
                    cv2.imshow('Received Image', self.img)  # 画像を表示
                    cv2.waitKey(1)  # 表示を更新
                    i += 1

        finally:
            client_socket.close()
            cv2.destroyAllWindows()

    def update_image(self):
        self.tk_image = ImageTk.PhotoImage(self.img)
        self.image_label.config(image=self.tk_image)

        self.root.after(20,self.update_image)
    
    def close(self):
        self.running = 0

if __name__ == '__main__':
    root = tk.Tk()
    window = Window(root)
    root.mainloop()