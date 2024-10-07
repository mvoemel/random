package server.http;


import server.constants.Method;

import java.net.URI;
import java.util.List;
import java.util.Map;

public class Request {
    private final Method httpMethod;
    private final URI uri;
    private final Map<String, List<String>> requestHeaders;
    private Request(Method opCode,
                    URI uri,
                    Map<String, List<String>> requestHeaders)
    {
        this.httpMethod = opCode;
        this.uri = uri;
        this.requestHeaders = requestHeaders;
    }

    public URI getUri() {
        return uri;
    }

    public Method getHttpMethod() {
        return httpMethod;
    }

    public Map<String, List<String>> getRequestHeaders() {
        return requestHeaders;
    }

    public static class Builder {
        private Method httpMethod;
        private URI uri;
        private Map<String, List<String>> requestHeaders;

        public Builder() {
        }

        public void setHttpMethod(Method httpMethod) {
            this.httpMethod = httpMethod;
        }

        public void setUri(URI uri) {
            this.uri = uri;
        }

        public void setRequestHeaders(Map<String, List<String>> requestHeaders) {
            this.requestHeaders = requestHeaders;
        }

        public Request build() {
            return new Request(httpMethod, uri, requestHeaders);
        }
    }
}