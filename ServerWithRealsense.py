import socket
import struct
import threading
import pyrealsense2 as rs
import cv2
import numpy as np

FRAME_RATE = 30

def send_video(client_socket):
    try:
        pipe = rs.pipeline()
        cfg = rs.config()
        cfg.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, FRAME_RATE)
        cfg.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, FRAME_RATE)

        pipe.start(cfg)

        while True:
            frames = pipe.wait_for_frames()
            color_frame = frames.get_color_frame()
            depth_frame = frames.get_depth_frame()

            # Convert color frame to numpy array
            color_image = np.asanyarray(color_frame.get_data())
            depth_image = np.asanyarray(depth_frame.get_data())

            # Encode frame as JPEG
            _, encoded_frame = cv2.imencode(".jpg", color_image)
            # _, encoded_frame = cv2.imencode(".jpg", depth_image)


            # Get size of the encoded frame
            size = len(encoded_frame)

            # Send size of the frame
            client_socket.sendall(struct.pack("!I", size))

            # Send the encoded frame
            client_socket.sendall(encoded_frame.tobytes())

    except Exception as e:
        print("Error sending video frames:", e)

    finally:
        pipe.stop()
        client_socket.close()

def main():
    server_address = ('192.168.66.179', 12345)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(server_address)
    server_socket.listen(1)
    print("Server is listening on", server_address)

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print("Connected to client", client_address)

            # Start a new thread to handle each client
            send_thread = threading.Thread(target=send_video, args=(client_socket,))
            send_thread.start()

    except Exception as e:
        print("Server error:", e)

    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
