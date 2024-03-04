import javafx.application.Application;
import javafx.application.Platform;
import javafx.scene.Scene;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.layout.StackPane;
import javafx.stage.Stage;

import java.io.DataInputStream;
import java.io.IOException;
import java.net.Socket;

public class VideoClient extends Application {

    private ImageView imageView;

    @Override
    public void start(Stage primaryStage) {
        String serverAddress = "192.168.66.214";
        int serverPort = 12345;

        imageView = new ImageView();
        StackPane root = new StackPane(imageView);
        Scene scene = new Scene(root, 640, 480);
        primaryStage.setScene(scene);
        primaryStage.setTitle("Video Client");
        primaryStage.setOnCloseRequest(e -> System.exit(0));
        primaryStage.show();

        new Thread(() -> {
            try {
                Socket socket = new Socket(serverAddress, serverPort);
                System.out.println("Connected to server.");

                DataInputStream inputStream = new DataInputStream(socket.getInputStream());

                while (true) {
                    // Receive the size of the frame
                    int size = inputStream.readInt();

                    // Receive the frame data
                    byte[] frameData = new byte[size];
                    inputStream.readFully(frameData);

                    // Update UI on JavaFX Application Thread
                    Platform.runLater(() -> {
                        // Convert byte array to Image and display
                        Image image = new Image(frameData);
                        imageView.setImage(image);
                    });
                }

            } catch (IOException e) {
                e.printStackTrace();
            }
        }).start();
    }

    public static void main(String[] args) {
        launch(args);
    }
}
