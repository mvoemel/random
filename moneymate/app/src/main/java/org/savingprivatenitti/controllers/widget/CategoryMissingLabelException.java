package org.savingprivatenitti.controllers.widget;

/**
 * Exception class that is thrown when a category is missing a label.
 */
public class CategoryMissingLabelException extends RuntimeException {
    /**
     * Constructor for the CategoryMissingLabelException exception class.
     *
     * @param message The exception message.
     */
    public CategoryMissingLabelException(String message) {
        super(message);
    }
}
