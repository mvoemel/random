package org.savingprivatenitti.models;

import javafx.scene.paint.Color;

import java.util.Objects;

public record Category(int id, String label, Color color) implements Comparable<Category> {

    @Override
    public int compareTo(Category other) {
        return this.label().compareTo(other.label());
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Category category = (Category) o;
        return Objects.equals(id, category.id);
    }

    @Override
    public int hashCode() {
        return Objects.hash(label);
    }
}
