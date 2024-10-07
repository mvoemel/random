package server.constants;

/**
 * Map of status code values and meanings.
 */
//public class StatusCode {
//
//    public static final Map<Integer, String> STATUS_CODES = Map.of(
//            200, "OK",
//            400, "BAD_REQUEST",
//            404, "NOT_FOUND",
//            500, "INTERNAL_SERVER_ERROR"
//    );
//}

public enum StatusCode {
    OK(200),
    BAD_REQUEST(400),
    NOT_FOUND(404),
    INTERNAL_SERVER_ERROR(500);

    private final int code;

    StatusCode(int code) {
        this.code = code;
    }

    public int getCode() {
        return code;
    }

    // Method to get the enum constant from the code
    public static StatusCode fromCode(int code) {
        for (StatusCode status : StatusCode.values()) {
            if (status.getCode() == code) {
                return status;
            }
        }
        throw new IllegalArgumentException("No matching status code for: " + code);
    }
}