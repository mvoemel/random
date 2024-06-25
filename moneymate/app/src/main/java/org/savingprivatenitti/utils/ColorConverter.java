package org.savingprivatenitti.utils;

import javafx.scene.paint.Color;

public class ColorConverter {

    /**
     * Convert a JavaFX color object to an array of RGB components
     * @param color the color to convert
     * @return an array of RGB components
     */
    public static int[] toRGBComponents(Color color) {
        return new int[]{
                (int) (color.getRed() * 255),
                (int) (color.getGreen() * 255),
                (int) (color.getBlue() * 255)
        };
    }

    /**
     * Convert a JavaFX color object to a hex code
     * @param color the color to convert
     * @return the hex code of the color
     */
    public static String toHex(Color color) {
        return String.format("#%02X%02X%02X",
                (int) (color.getRed() * 255),
                (int) (color.getGreen() * 255),
                (int) (color.getBlue() * 255));
    }
}
