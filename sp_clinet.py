import socket
import numpy as np
import cv2
import threading
import tkinter as tk
from PIL import ImageTk, Image
import time

# ソケットの設定
ipaddr = "192.168.76.68"
port = 8000
socket_path = ((ipaddr,8000))

class Window():
    def __init__(self,root,img_f,height,weight):
        self.root = root
        self.img_f = img_f
        self.height = height
        self.weight = weight

        self.image_label = tk.Label(self.img_f)
        self.image_label.pack()
        self.flag = False
        self.running = True
        threading.Thread(target=self.receive_images,daemon=True).start()
        self.update_image()

    def receive_images(self):
        # ソケットの作成
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((ipaddr,8000))

        try:
            while self.running:
                # データを受信
                data = bytearray()
                while self.running:
                    try:
                        # 受信データを逐次追加
                        packet = self.client_socket.recv(4096)
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
            self.client_socket.close()
            cv2.destroyAllWindows()
            
    def update_image(self):
        if self.flag:
            self.flag = False
            try:
                self.img = cv2.cvtColor(self.img,cv2.COLOR_BGR2RGB)
                pil_img = Image.fromarray(self.img)
                self.tk_image = ImageTk.PhotoImage(pil_img)
                self.image_label.config(image=self.tk_image)
            except cv2.error as e:
                print(e)
        self.root.after(20,self.update_image)

    def send_command(self,cmd):
        self.client_socket.sendall((cmd+"fin").encode('utf-8'))
        print(f"コマンド:{cmd}")
    
    def close(self):
        self.running = False

if __name__ == '__main__':
    root = tk.Tk()
    window = Window(root)
    root.mainloop()
    window.close()