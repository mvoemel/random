package org.savingprivatenitti.controllers.utils;

import org.junit.jupiter.api.Test;
import org.savingprivatenitti.utils.TextFormatter;
import javafx.scene.text.Font;

import static org.junit.jupiter.api.Assertions.*;

public class TextFormatterTest {

    @Test
    public void testShortenTextToFit() {
        String text = "This is a very long text that should be shortened to fit the given width.";
        Font font = Font.font("Arial", 12);
        double maxWidth = 100;

        String shortenedText = TextFormatter.shortenTextToFit(text, maxWidth, font);

        assertTrue(shortenedText.length() < text.length()); // The shortened text should be shorter than the original text
        assertTrue(shortenedText.endsWith("...")); // The shortened text should end with "..."
    }
}