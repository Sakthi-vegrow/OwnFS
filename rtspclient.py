from rtsp.server import Server

# Define the path to the video file
VIDEO_FILE_PATH = 'path/to/your/video/file.mp4'

# Define RTSP server parameters
SERVER_IP = '0.0.0.0'
SERVER_PORT = 8554

# Create a new RTSP server instance
server = Server()

# Add a video stream to the server
server.add_application("live")

# Specify the video file to stream
server.add_stream("live", VIDEO_FILE_PATH)

# Start the server
server.start(SERVER_IP, SERVER_PORT)
