import java.net.*;
import java.io.*;

public class Client {
    private static final String SERVER_ADDRESS = "141.145.200.6";
    private static final int SERVER_PORT = 8000;

    public static void main(String[] args) throws IOException {
        try {
            //create socket and connect to server
            Socket socket = new Socket(SERVER_ADDRESS, SERVER_PORT);
            System.out.println("Connected to server.");
            //data recive untill recive  new line caractor
            BufferedReader BReader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            //print data recived for reader variable
            String MyUrl = BReader.readLine();
            System.out.println("recived data : " + MyUrl);
            //socket close
            socket.close();
            try {
                // MyUrl = "http://localhost:5000/download?ID=123";
                URL url = new URL(MyUrl);
                HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                conn.setRequestMethod("GET");
                if (conn.getResponseCode() == HttpURLConnection.HTTP_OK) {
                    String fileName = "5MB.zip";
                    InputStream inputStream = conn.getInputStream();
                    FileOutputStream outputStream = new FileOutputStream(fileName);
                    byte[] buffer = new byte[1024];
                    int bytesRead = -1;
                    while ((bytesRead = inputStream.read(buffer)) != -1) {
                        outputStream.write(buffer, 0, bytesRead);
                    }
                    outputStream.close();
                    inputStream.close();
                    System.out.println("File downloaded successfully.");
                } else {
                    System.out.println("Failed to download file. Response code: " + conn.getResponseCode());
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        } catch (UnknownHostException e) {
            System.err.println("ERROR: Server not found.");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}