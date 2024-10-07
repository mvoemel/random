package server;

import server.http.Handler;
import server.constants.Method;
import server.http.RequestRunner;

import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.Executor;
import java.util.concurrent.Executors;

/*
 * Simple Server: accepts HTTP connections and responds using
 * the Java net socket library.
 *  - Blocking approach ( 1 request per thread )
 *  - Non-blocking ( Investigate Java NIO - new IO, Netty uses this? )
 */
public class Server {

    private final Map<String, RequestRunner> routes;
    private final ServerSocket socket;
    private final Executor threadPool;
    private Handler handler;

    public Server(int port, int nThreads) throws IOException {
        routes = new HashMap<>();
        threadPool = Executors.newFixedThreadPool(nThreads);
        socket = new ServerSocket(port);
    }

    public Server(int port) throws IOException {
        this(port, 100);
    }

    public void start() throws IOException {
        handler = new Handler(routes);

        while (true) {
            Socket clientConnection = socket.accept();
            handleConnection(clientConnection);
        }
    }

    /*
     * Capture each Request / Response lifecycle in a thread
     * executed on the threadPool.
     */
    private void handleConnection(Socket clientConnection) {
        Runnable httpRequestRunner = () -> {
            try {
                handler.handleConnection(clientConnection.getInputStream(), clientConnection.getOutputStream());
            } catch (IOException ignored) {
            }
        };
        threadPool.execute(httpRequestRunner);
    }

    public void addRoute(final Method opCode, final String route, final RequestRunner runner) {
        routes.put(opCode.name().concat(route), runner);
    }
}