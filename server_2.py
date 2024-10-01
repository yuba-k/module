from picamera import PiCamera
import socket
import base64
import time
import cv2
import motor
import configparser
import threading

# picamera.capture_continuous()
# https://qiita.com/uneyamauneko/items/411edbc695f1222535df
# https://code.tiblab.net/python/raspi/picamera/capture
# https://picamera.readthedocs.io/en/release-1.13/api_camera.html
# https://picamera.readthedocs.io/en/release-1.13/recipes1.html
class Server():
    def __init__(self):
        self.cap = PiCamera()
        self.cap.resolution = (320,240)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        ipaddr = "192.168.156.132"
        self.s.bind((ipaddr,63000))
        self.s.listen(1)
        self.conn,_ =  self.s.accept()
        config = configparser.ConfigParser()
        #設定ファイル読み込み
        config.read("cansat_config.ini")
        self.motor_cont = motor.Motor(config)

    def encode_send(self):
        i = 0
        while True:
            self.cap.capture(f"/send_pic/cap{i}.jpg")
            with open(f"/send_pic/cap{i}.jpg",'rb') as f:
                encode = base64.urlsafe_b64encode(f.read())
            self.conn.send(encode)
            self.conn.sendall(b"end_to_send")
            print("受け渡し終わり")
            i += 1

    def closed(self):
        self.s.close()
    
    def listen(self):
        command = self.conn.recv(64).decode()
        self.motor_cont.move(command,5)

def main():
    try:
        print("コードスタート")
        server = Server()
        thread1 = threading.Thread(target=server.encode_send)
        thread2 = threading.Thread(target=server.listen)
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()
    except KeyboardInterrupt:
        server.closed()
        print("接続断")
        

if __name__ == "__main__":
    main()