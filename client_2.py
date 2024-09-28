import socket
import tkinter as tk
import base64
import ctypes
import numpy as np
import cv2
import threading
import time
from PIL import Image, ImageTk
import binascii
"""
Created     : 2024/08/23
Accuracy    : Full of a handmade feel
              Display updates at about 3 fps
              Latency is about 0.5 seconds (or less)
Description : Display with 320*240 screen size and image data
Image Format: JPG (PGM, PPM, GIF and PNG  is OK)
Restriction : Images may be distorted at 3 fps or more 
              (however, reception (decoding) will be processed normally)
"""
class Display():
    def __init__(self,root):
        self.root = root
        self.root.title("test_window")
        self.root.geometry("320x240")
        self.number = 0
        ctypes.windll.shcore.SetProcessDpiAwareness(1)

    def window(self):
        print("画面生成開始")
        self.img_canvas = tk.Canvas(
            self.root,
            width=320,
            height=240,
            bg="black"
        )
        self.img_canvas.place(x=0,y=0)
        self.image_on_canvas = self.img_canvas.create_image(
            0,
            0,
            anchor=tk.NW
        )
        self.updata()

    def updata(self):
        print(f"updata実行:{self.number}")
        r_img = cv2_to_tk(self.number)
        if r_img == "Null":
            pass
        else:
            self.img = r_img
            self.img_canvas.itemconfigure(       
                self.image_on_canvas,
                image=self.img,  # 表示画像データ
            )
            self.img_canvas.update()
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
    def __init__(self):
        ip = "192.168.24.132"
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
                try:
                    data = self.s.recv(1024)
                    if b"end_to_send" in data:
                        data = data.replace(b"end_to_send",b"===========")
                        save_img = base64.urlsafe_b64decode(data)
                        f.write(save_img)
                        self.s.sendall(b'next')
                        break
                    save_img = base64.urlsafe_b64decode(data)
                    f.write(save_img)
                except binacii.Error:
                    pass
        print("デコード&受け取り終わり")

def main():
    try:
        root = tk.Tk()
        display = Display(root)
        reciver = Reciver()
        stop_event = threading.Event()#強制停止の準備
        display.window()
        # thread1 = threading.Thread(target=display.window)
        thread2 = threading.Thread(target=reciver.work)
        # thread1.start()
        thread2.start()
        root.mainloop()
        # thread1.join()
        thread2.join()
        print("all finish")
    except KeyboardInterrupt:
        stop_event.set()
        print("\nKeyboardInterrupt")

if __name__ == "__main__":
    main()