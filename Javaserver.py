import cv2
import socket
import struct
import threading
import time

import time

FRAME_RATE = 30
def send_video(client_socket, video_file):
    try:
        # cap = cv2.VideoCapture(video_file)
        cap = cv2.VideoCapture(0)
        frame_num = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            if frame is None:
                print("Failed to decode frame.")
                continue
            _, encoded_frame = cv2.imencode(".jpg", frame)

            size = len(encoded_frame)
            print("Sending frame", frame_num)
            client_socket.sendall(struct.pack("!I", size))

            client_socket.sendall(encoded_frame.tobytes())
            frame_num += 1
            time.sleep(1 / FRAME_RATE)

    except Exception as e:
        print("Error sending video frames:", e)

    finally:
        cap.release()
        client_socket.close()

def main():
    video_file = "./sample.mp4"

    server_address = ('192.168.66.214', 12345)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(server_address)
    server_socket.listen(1)

    print("Server is listening on", server_address)

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print("Connected to client", client_address)

            send_thread = threading.Thread(target=send_video, args=(client_socket, video_file))
            send_thread.start()

    except Exception as e:
        print("Server error:", e)

    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
