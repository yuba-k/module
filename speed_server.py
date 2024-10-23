import picamera
import picamera.array
import socket
import time
import cv2
import threading
import motor
import configparser

# ソケットの設定
ipaddr = "192.168.76.68"
port = 8000
socket_path = ((ipaddr,8000))

connection = None

flag = False

def start_camera():
    global connection
    global flag
    # カメラの初期設定
    camera = picamera.PiCamera()
    camera.resolution = (640, 480)  # 解像度を640x480に設定
    camera.framerate = 10  # フレームレートを60fpsに設定
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
        flag = True


        try:
            for frame in camera.capture_continuous(stream, format='bgr', use_video_port=True):
                # フレームをJPEGにエンコード
                img = stream.array
                _, img_encoded = cv2.imencode('.jpg', img)

                # クライアントに送信
                connection.sendall(img_encoded.tobytes())
                stream.truncate(0)  # ストリームをリセット
                connection.sendall(b"fin")
        except KeyboardInterrupt as e:
            print(e)
            flag = False
        finally:
            connection.close()
            server_socket.close()
            camera.close()

def listen(motor_control):
    global connection
    global flag
    print("読み込まれたよ!")
    
    cmd = ""  # cmdの初期化
    while True:
        if flag:
            while True:
                try:
                    # 受信データをバッファサイズを調整して受信
                    reccmd = connection.recv(1024).decode()  # バッファサイズを増やす
                    if not reccmd:
                        print("接続が閉じられました。")
                        return
                except KeyboardInterrupt as e:
                    print(e)
                    return
                except Exception as e:
                    print(f"エラー: {e}")
                    break
                print("b")
                # "fin"が受信された場合、コマンドを保存
                if "fin" in reccmd:
                    cmd += reccmd.replace("fin", "")
                    print(f"受信:{cmd}")
                    motor_control.move(cmd, 2)
                    cmd = ""  # コマンドを処理後にリセット
                    break  # コマンドを処理したのでループを抜ける
        time.sleep(0.1)



if __name__ == '__main__':
    #ConfigParserオブジェクトを生成
    config = configparser.ConfigParser()

    #設定ファイル読み込み
    config.read("cansat_config.ini")
    motor = motor.Motor(config)

    thread1 = threading.Thread(target=start_camera,daemon=True)
    thread1.start()
    listen(motor)
    thread1.join()
    motor.cleanup()