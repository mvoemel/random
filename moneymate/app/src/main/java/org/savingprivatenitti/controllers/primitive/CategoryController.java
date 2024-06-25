package org.savingprivatenitti.controllers.primitive;

import javafx.fxml.FXML;
import javafx.scene.control.Label;
import javafx.scene.layout.AnchorPane;
import org.savingprivatenitti.models.Category;
import org.savingprivatenitti.utils.ColorConverter;

public class CategoryController {

    @FXML
    private Label categoryLabel;

    @FXML
    private AnchorPane categoryBox;

    /**
     * Add category data to the category
     * @param category the category to add
     */
    public void addCategoryDataToCategory(Category category) {
        categoryLabel.setText(category.label());
        applyCategoryStyles(category);
    }

    /**
     * Apply the styles to the category
     * @param category the category to apply the styles to
     */
    public void applyCategoryStyles(Category category) {
        String hexColor = ColorConverter.toHex(category.color());
        int[] rgbComponents = ColorConverter.toRGBComponents(category.color());
        double opacity = 0.2;

        String newStyle = "-fx-background-color: rgba(" + rgbComponents[0] + ", " + rgbComponents[1] + ", " + rgbComponents[2] + ", " + opacity + ");"
                + "-fx-border-color: rgba(" + rgbComponents[0] + ", " + rgbComponents[1] + ", " + rgbComponents[2] + ");"
                + "-fx-border-radius: 4;"
                + "-fx-background-radius: 4;";
        categoryBox.setStyle(newStyle);

        newStyle = "-fx-text-fill: " + hexColor + ";";
        categoryLabel.setStyle(newStyle);
    }
}
