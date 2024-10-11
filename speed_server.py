import picamera
import picamera.array
import socket
import time
import cv2
import threading
import motor
import configparser

# ソケットの設定
ipaddr = "192.168.29.38"
port = 8000
socket_path = ((ipaddr,8000))

global server_socket

def start_camera():
    global server_socket
    # カメラの初期設定
    camera = picamera.PiCamera()
    camera.resolution = (640, 480)  # 解像度を640x480に設定
    camera.framerate = 30  # フレームレートを60fpsに設定
    camera.exposure_mode = 'auto' #露出モード
    camera.meter_mode = 'average' #測光モード
    camera.awb_mode = 'fluorescent'

    # ストリームを作成
    with picamera.array.PiRGBArray(camera) as stream:
        time.sleep(2)  # カメラのウォームアップ

        # ソケットの作成
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((ipaddr,8000))
        server_socket.listen(1)

        print("Waiting for a connection...")
        connection, client_address = server_socket.accept()
        print("Connection established!")

        try:
            for frame in camera.capture_continuous(stream, format='bgr', use_video_port=True):
                # フレームをJPEGにエンコード
                img = stream.array
                _, img_encoded = cv2.imencode('.jpg', img)

                # クライアントに送信
                connection.sendall(img_encoded.tobytes())
                stream.truncate(0)  # ストリームをリセット
                connection.sendall(b"fin")

        finally:
            connection.close()
            server_socket.close()
            camera.close()

def listen(motor_control):
    global server_socket
    while True:
        cmd = server_socket.recv(64)
        print(cmd.decode())
        motor_control.move(cmd.decode(),2)


if __name__ == '__main__':
    #ConfigParserオブジェクトを生成
    config = configparser.ConfigParser()

    #設定ファイル読み込み
    config.read("cansat_config.ini")
    motor = motor.Motor(config)
    thread1 = threading.Thread(target=lambda:listen(motor),daemon=True)
    thread2 = threading.Thread(target=start_camera(),daemon=True)
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()