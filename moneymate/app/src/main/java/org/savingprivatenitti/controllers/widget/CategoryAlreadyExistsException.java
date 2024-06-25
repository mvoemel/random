package org.savingprivatenitti.controllers.widget;


/**
 * Exception class that is thrown when a category already exists.
 */
public class CategoryAlreadyExistsException extends RuntimeException {
    /**
     * Constructor for the CategoryAlreadyExistsException exception class.
     *
     * @param message The exception message.
     */
    public CategoryAlreadyExistsException(String message) {
        super(message);
    }
}