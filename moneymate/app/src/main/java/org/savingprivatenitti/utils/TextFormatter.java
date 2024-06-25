package org.savingprivatenitti.utils;

import javafx.scene.text.Font;
import javafx.scene.text.Text;

import java.util.logging.Level;
import java.util.logging.Logger;

public class TextFormatter {

    /**
     * Shorten the text to fit the given width
     * @param text The text to shorten
     * @param maxWidth The maximum width of the text
     * @param font The font of the text
     * @return The shortened text
     */
    public static String shortenTextToFit(String text, double maxWidth, Font font) {
        Text helper = new Text();
        helper.setFont(font);
        helper.setText(text);

        if (helper.getLayoutBounds().getWidth() <= maxWidth) {
            Logger.getLogger(TextFormatter.class.getName()).log(Level.INFO, "Text unchanged. Text does not exceed maxWidth");
            return text;
        }

        String suffix = "...";
        for (int i = text.length(); i > 0; i--) {
            helper.setText(text.substring(0, i) + suffix);
            if (helper.getLayoutBounds().getWidth() <= maxWidth) {
                return helper.getText();
            }
        }
        Logger.getLogger(TextFormatter.class.getName()).log(Level.INFO, "Text shortened. Text exceeded maxWidth");
        return suffix;
    }

}
