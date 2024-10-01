import picamera
import picamera.array
import socket
import time

# ソケットの設定
socket_path = '/tmp/ram/camera.sock'

def start_camera():
    # カメラの初期設定
    camera = picamera.PiCamera()
    camera.resolution = (640, 480)  # 解像度を640x480に設定
    camera.framerate = 60  # フレームレートを60fpsに設定

    # ストリームを作成
    with picamera.array.PiRGBArray(camera) as stream:
        time.sleep(2)  # カメラのウォームアップ

        # ソケットの作成
        server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        server_socket.bind(socket_path)
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

        finally:
            connection.close()
            server_socket.close()
            camera.close()

if __name__ == '__main__':
    start_camera()
