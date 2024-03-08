import cv2
import socket
import struct
import numpy as np
import time

# Define the frame rate of the video
FRAME_RATE = 30  # Adjust this value according to the frame rate of your video

def receive_video(client_socket):
    while True:
        # Receive the size of the frame data
        size_data = client_socket.recv(4)
        if not size_data:
            break

        # Unpack the size of the frame data
        size = struct.unpack("!I", size_data)[0]

        # Receive the frame data
        data = b""
        while len(data) < size:
            packet = client_socket.recv(size - len(data))
            if not packet:
                break
            data += packet

        # Convert the received data back into a numpy array
        encoded_frame = np.frombuffer(data, dtype=np.uint8)

        # Decode the encoded frame
        frame = cv2.imdecode(encoded_frame, cv2.IMREAD_COLOR)

        # Check if frame decoding was successful
        if frame is None:
            print("Failed to decode frame.")
            continue

        # Flip the frame horizontally
        frame = cv2.flip(frame, 1)

        # Display the received frame
        cv2.imshow("Received Video", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Introduce a delay to match the original frame rate
        time.sleep(1 / FRAME_RATE)

    cv2.destroyAllWindows()


def main():
    # Server address and port
    server_address = ('10.20.121.125', 12345)

    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect(server_address)

    print("Connected to server.")

    # Receive and display video from the server
    receive_video(client_socket)

    # Cleanup
    client_socket.close()

if __name__ == "__main__":
    main()
