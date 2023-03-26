import java.io.*;
import org.json.*;

public class Main {
    public static void main(String[] args) {
        try {
            // Create the process builder
            ProcessBuilder processBuilder = new ProcessBuilder("python", "sock99k.py");

            // Start the process
            Process process = processBuilder.start();

            // Get the input stream of the process
            InputStream inputStream = process.getInputStream();
            BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream));

            // Read the output of the Python script line by line
            String line;
            while ((line = reader.readLine()) != null) {
                JSONObject jsonObject = new JSONObject(line);
                JSONArray dataArray = jsonObject.getJSONArray("Data");
                String data = dataArray.get(0).toString();
                if (data.equals("USERID")) System.out.println("USER ID : "+dataArray.get(1).toString());
                if (data.equals("SENDMOBILEMODELPARAMETERS")){
                    System.out.println("RECIVED MOBILE MODEL PARAMETERS");
                }
            }

            // Wait for the process to complete and get the exit code
            int exitCode = process.waitFor();
            System.out.println("Python script exited with code " + exitCode);
        } catch (IOException e) {
            e.printStackTrace();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}
