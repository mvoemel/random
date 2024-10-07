package app;

import server.Server;
import server.http.Response;

import java.io.IOException;

import static server.constants.Method.GET;

public class App {
    public static void main(String[] args) throws IOException {
        Server myServer = new Server(8080);
        myServer.addRoute(GET, "/hello-world",
                (req) -> new Response.Builder()
                        .setStatusCode(200)
                        .addHeader("Content-Type", "text/html")
                        .setEntity("<HTML> <P> Hello World! 123 </P> </HTML>")
                        .build());
        myServer.start();
    }
}
