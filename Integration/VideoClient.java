import javax.swing.*;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.ByteArrayInputStream;
import java.io.DataInputStream;
import java.io.IOException;
import java.net.Socket;
import javax.imageio.ImageIO;

public class VideoClient {

    public static void main(String[] args) {
        String serverAddress = "192.168.66.217";
        int serverPort = 12345;

        try {
            Socket socket = new Socket(serverAddress, serverPort);
            System.out.println("Connected to server.");

            DataInputStream inputStream = new DataInputStream(socket.getInputStream());

            // Create a JFrame to display the video
            JFrame frame = new JFrame("Video");
            frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            frame.setSize(640, 480);
            
            // Create a JLabel to hold the video frames
            JLabel label = new JLabel();
            frame.add(label);
            frame.setVisible(true);

            while (true) {
                // Receive the size of the frame
                int size = inputStream.readInt();
                System.out.println("Size: "+size);

                // Receive the frame data
                byte[] frameData = new byte[size];
                inputStream.readFully(frameData);

                // Convert byte array to BufferedImage
                ByteArrayInputStream byteArrayInputStream = new ByteArrayInputStream(frameData);
                BufferedImage image = ImageIO.read(byteArrayInputStream);

                // Mirror the image horizontally
                BufferedImage mirroredImage = new BufferedImage(image.getWidth(), image.getHeight(), BufferedImage.TYPE_INT_RGB);
                Graphics2D g = mirroredImage.createGraphics();
                g.drawImage(image, 0, 0, image.getWidth(), image.getHeight(), image.getWidth(), 0, 0, image.getHeight(), null);
                g.dispose();

                // Update the JLabel with the new frame
                label.setIcon(new ImageIcon(mirroredImage));
            }

        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}