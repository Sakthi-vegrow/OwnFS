import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.List;

public class getIP {

    public static void main(String[] args) {
        try {
            // Build the command
            List<String> command = List.of("bash", "-c", "ifconfig");

            // Start the process
            ProcessBuilder processBuilder = new ProcessBuilder(command);
            Process process = processBuilder.start();

            // Read the output of the command
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String line;
            while ((line = reader.readLine()) != null) {
                // Find the line containing the IP address
                if (line.contains("inet ") && !line.contains("127.0.0.1")) {
                    // Extract and print the IP address
                    String ipAddress = line.trim().split("\\s+")[1];
                    System.out.println("IP Address: " + ipAddress);
                }
            }

            // Wait for the process to complete
            int exitCode = process.waitFor();
            System.out.println("Command executed with exit code: " + exitCode);
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }
    }
}
