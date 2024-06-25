package org.savingprivatenitti.controllers.models;

import org.junit.jupiter.api.Test;
import org.savingprivatenitti.models.Category;
import javafx.scene.paint.Color;

import java.util.Objects;

import static org.junit.jupiter.api.Assertions.*;

public class CategoryTest {

    @Test
    public void testCompareTo() {
        Category category1 = new Category(1, "Food", Color.RED);
        Category category2 = new Category(2, "Rent", Color.BLUE);

        assertTrue(category1.compareTo(category2) < 0);
    }

    @Test
    public void testEquals() {
        Category category1 = new Category(1, "Food", Color.RED);
        Category category2 = new Category(1, "Rent", Color.BLUE);

        assertEquals(category1, category2);
    }

    @Test
    public void testHashCode() {
        Category category = new Category(1, "Food", Color.RED);
        int expected = Objects.hash("Food");

        assertEquals(expected, category.hashCode());
    }
}