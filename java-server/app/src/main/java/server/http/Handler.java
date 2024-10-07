package server.http;



import java.io.*;
import java.util.Map;
import java.util.Optional;

/**
 * Handle HTTP Request Response lifecycle.
 */
public class Handler {

    private final Map<String, RequestRunner> routes;

    public Handler(final Map<String, RequestRunner> routes) {
        this.routes = routes;
    }
    public void handleConnection(final InputStream inputStream, final OutputStream outputStream) throws IOException {
        final BufferedWriter bufferedWriter = new BufferedWriter(new OutputStreamWriter(outputStream));

        Optional<Request> request = Decoder.decode(inputStream);
        request.ifPresentOrElse((r) -> handleRequest(r, bufferedWriter), () -> handleInvalidRequest(bufferedWriter));

        bufferedWriter.close();
        inputStream.close();
    }
    private void handleInvalidRequest(final BufferedWriter bufferedWriter) {
        Response notFoundResponse = new Response.Builder().setStatusCode(400).setEntity("Invalid Request...").build();
        ResponseWriter.writeResponse(bufferedWriter, notFoundResponse);
    }

    private void handleRequest(final Request request, final BufferedWriter bufferedWriter) {
        final String routeKey = request.getHttpMethod().name().concat(request.getUri().getRawPath());

        if (routes.containsKey(routeKey)) {
            ResponseWriter.writeResponse(bufferedWriter, routes.get(routeKey).run(request));
        } else {
            // Not found
            ResponseWriter.writeResponse(bufferedWriter, new Response.Builder().setStatusCode(404).setEntity("Route Not Found...").build());
        }
    }
}