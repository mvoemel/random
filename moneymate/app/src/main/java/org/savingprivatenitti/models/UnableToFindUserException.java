package org.savingprivatenitti.models;

/**
 * Exception class that is thrown when a user cannot be found.
 */
public class UnableToFindUserException extends RuntimeException {
    /**
     * Constructor for the UnableToFindUserException exception class.
     *
     * @param message The exception message.
     */
    public UnableToFindUserException(String message) {
        super(message);
    }
}
