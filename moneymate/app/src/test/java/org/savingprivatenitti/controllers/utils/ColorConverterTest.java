package org.savingprivatenitti.controllers.utils;

import org.junit.jupiter.api.Test;
import org.savingprivatenitti.utils.ColorConverter;
import javafx.scene.paint.Color;

import static org.junit.jupiter.api.Assertions.*;

public class ColorConverterTest {

    @Test
    public void testToRGBComponents() {
        Color color = Color.rgb(255, 0, 0); // Red color
        int[] expected = new int[]{255, 0, 0};
        assertArrayEquals(expected, ColorConverter.toRGBComponents(color));
    }

    @Test
    public void testToHex() {
        Color color = Color.rgb(255, 0, 0); // Red color
        String expected = "#FF0000";
        assertEquals(expected, ColorConverter.toHex(color));
    }
}