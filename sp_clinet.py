import socket
import numpy as np
import cv2
import threading
import tkinter as tk
from PIL import ImageTk, Image
import time

# ソケットの設定
ipaddr = "192.168.171.38"
port = 8000
socket_path = ((ipaddr,8000))

class Window():
    def __init__(self,root):
        self.root = root
        self.image_label = tk.Label(self.root)
        self.image_label.pack()
        self.flag = False
        self.running = True
        threading.Thread(target=self.receive_images).start()
        self.cheaker()

    def receive_images(self):
        # ソケットの作成
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ipaddr,8000))

        try:
            while self.running:
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
                if data:
                    self.img_array = np.frombuffer(data, np.uint8)
                    self.img = cv2.imdecode(self.img_array, cv2.IMREAD_COLOR)

                    if self.img is not None:
                        self.flag = True
                    #     self.update_image()
                else:
                    print("none image")

        finally:
            client_socket.close()
            cv2.destroyAllWindows()

    def cheaker(self):
        while True:
            if self.flag == True:
                self.update_image()
                break
            time.sleep(0.2)
            
    def update_image(self):
        try:
            self.img = cv2.cvtColor(self.img,cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(self.img)
            self.tk_image = ImageTk.PhotoImage(pil_img)
            self.image_label.config(image=self.tk_image)
        except cv2.error as e:
            print(e)
        self.root.after(20,self.update_image)
    
    def close(self):
        self.running = False

if __name__ == '__main__':
    root = tk.Tk()
    window = Window(root)
    root.mainloop()
    window.close()