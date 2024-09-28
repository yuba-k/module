import socket
import tkinter as tk
import ctypes
import base64
import numpy as np
import cv2
import threading
import time
from PIL import Image, ImageTk
import binascii

class Disp():
    def __init__(self,root,canvas):
        self.root = root
        self.canvas = canvas
        self.number = 0
    def window(self):
        self.image_on_canvas = self.canvas.create_image(
            0,
            0,
            anchor = tk.NW
        )
        self.updata()
    def updata(self):
        r_img = cv2_to_tk(self.number)
        if r_img == "Null":
            pass
        else:
            self.img = r_img
            self.canvas.itemconfigure(       
                self.image_on_canvas,
                image=self.img,  # 表示画像データ
            )
            self.canvas.update()
            self.number += 1
        self.root.after(300,self.updata)

def cv2_to_tk(num):
    try:
        cv2_img = cv2.imread(f"decode{num}.jpg")
        rgb_cv2_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
        # NumPy配列からPIL画像オブジェクトを生成
        pil_img = Image.fromarray(rgb_cv2_img)
        # PIL画像オブジェクトをTkinter画像オブジェクトに変換
        tk_image = ImageTk.PhotoImage(pil_img)
        return tk_image
    except:
        return "Null"

class Reciver():
    def __init__(self,ip):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((ip, 63000))
        self.full_data = b""

    def work(self):
        self.j = 1
        while True:
            print(self.j)
            self.rec()
            time.sleep(0.05)
            self.j += 1

    def rec(self):
        print("受け取りはじめ")
        with open(f'decode{self.j}.jpg', mode='wb') as f:
            while True:
                data = self.s.recv(1024)
                if b"end_to_send" in data:
                    data = data.replace(b"end_to_send",b"===========")
                    save_img = base64.urlsafe_b64decode(data)
                    f.write(save_img)
                    self.s.sendall(b'next')
                    break
                save_img = base64.urlsafe_b64decode(data)
                f.write(save_img)
        print("デコード&受け取り終わり")

def main():
    root = tk.Tk()
    root.title("test")
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    canvas = tk.Canvas(
        root,
        width = 320,
        height = 240
    )
    canvas.pack()
    disp = Disp(root,canvas=canvas)
    disp.window()
    rec = Reciver(ip="192.168.57.132")
    thread = threading.Thread(target=rec.work)
    thread.start()
    root.mainloop()
    thread.join()


if __name__ == "__main__":
    main()