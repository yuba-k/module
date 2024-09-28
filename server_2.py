from picamera import PiCamera
import socket
import base64
import time
import cv2

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
        ipaddr = "192.168.24.132"
        self.s.bind((ipaddr,63000))
        self.s.listen(1)
        self.conn,_ =  self.s.accept()

    def encode_send(self,i):
        self.cap.capture(f"/send_pic/cap{i}.jpg")
        with open(f"/send_pic/cap{i}.jpg",'rb') as f:
            encode = base64.urlsafe_b64encode(f.read())
        self.conn.send(encode)
        self.conn.sendall(b"end_to_send")
        print("受け渡し終わり")

    def closed(self):
        self.s.close()

def main():
    try:
        print("コードスタート")
        server = Server()
        i = 0
        while True:
            print(i)
            server.encode_send(i)
            time.sleep(0.05)
            i += 1
    except KeyboardInterrupt:
        server.closed()
        print("接続断")
        

if __name__ == "__main__":
    main()