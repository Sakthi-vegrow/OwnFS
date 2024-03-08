import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Arrays;
import java.util.List;

public class connect_hotspot {

    public static void main(String[] args) {
        try {
            // Access point credentials
            String ssid = "vivo T2 Pro 5G ";
            String password = "sakthi123123";

            // Build the nmcli command
            List<String> command = Arrays.asList("nmcli", "device", "wifi", "connect", ssid, "password", password);

            // Start the process
            ProcessBuilder processBuilder = new ProcessBuilder(command);
            Process process = processBuilder.start();

            // Read the output of the command
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String line;
            while ((line = reader.readLine()) != null) {
                System.out.println(line);
            }

            // Wait for the process to complete
            int exitCode = process.waitFor();
            System.out.println("Command executed with exit code: " + exitCode);
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }
    }
}
