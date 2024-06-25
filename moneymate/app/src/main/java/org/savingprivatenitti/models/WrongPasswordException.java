package org.savingprivatenitti.models;

/**
 * Exception class that is thrown when a user is not found.
 */
public class WrongPasswordException extends RuntimeException {
    /**
     * Constructor for the WrongPasswordException exception class.
     *
     * @param message The exception message.
     */
    public WrongPasswordException(String message) {
        super(message);
    }
}
