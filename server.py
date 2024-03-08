import cv2
import socket
import struct
import threading
import time  # Import the time module

import time

# Define the frame rate of the video
FRAME_RATE = 30  # Adjust this value according to the frame rate of your video

def send_video(client_socket, video_file):
    try:
        # cap = cv2.VideoCapture(video_file)
        cap = cv2.VideoCapture(0)
        frame_num = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Check if frame decoding was successful
            if frame is None:
                print("Failed to decode frame.")
                continue

            # Display the received frame
            # cv2.imshow("Server Video", frame)

            # Introduce a delay to match the original frame rate
            # Encode the frame as JPEG
            _, encoded_frame = cv2.imencode(".jpg", frame)

            # Get the size of the encoded frame data
            size = len(encoded_frame)
/Users/sakthi/Downloads/VideoClient (1).java
            # Print the frame number
            print("Sending frame", frame_num)

            # Send the size of the frame data to the client
            client_socket.sendall(struct.pack("!I", size))

            # Send the frame data to the client
            client_socket.sendall(encoded_frame.tobytes())

            # Increment the frame number
            frame_num += 1

            # Introduce a delay to match the original frame rate
            time.sleep(1 / FRAME_RATE)

    except Exception as e:
        print("Error sending video frames:", e)

    finally:
        cap.release()
        client_socket.close()

def main():
    # Video file path
    video_file = "sample1.mp4"

    # Server address and port
    server_address = ('0.0.0.0', 12345)  # Listen on all available network interfaces

    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(server_address)
    server_socket.listen(1)

    print("Server is listening on", server_address)

    try:
        while True:
            # Accept a client connection
            client_socket, client_address = server_socket.accept()
            print("Connected to client", client_address)

            # Create a thread to send video from server to client
            send_thread = threading.Thread(target=send_video, args=(client_socket, video_file))
            send_thread.start()

    except Exception as e:
        print("Server error:", e)

    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
