package org.savingprivatenitti.controllers.listitem;

import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Node;
import javafx.scene.control.Button;
import javafx.scene.layout.HBox;
import org.savingprivatenitti.controllers.primitive.CategoryController;
import org.savingprivatenitti.models.Category;

import java.io.IOException;
import java.util.function.Consumer;
import java.util.logging.Level;
import java.util.logging.Logger;

public class CategoryListItemController {

    @FXML
    private HBox categoryListItemContainer;

    @FXML
    private Button categoryListItemDelete;

    private Consumer<Category> onDeleteCategory;

    private Category category;

    /**
     * Handle the event when the delete button is clicked
     */
    @FXML
    public void onCategoryDeleteButtonClicked() {
        if (onDeleteCategory != null) {
            onDeleteCategory.accept(category);
        } else {
            Logger.getLogger(CategoryListItemController.class.getName()).log(Level.SEVERE, "Error trying to delete category: onDeleteCategory consumer is not set");
            throw new RuntimeException("onDeleteCategory consumer is not set");
        }
    }

    /**
     * Set the consumer for the onDeleteCategory event
     *
     * @param onDeleteCategory the consumer for the onDeleteCategory event
     */
    public void setOnDeleteCategory(Consumer<Category> onDeleteCategory) {
        this.onDeleteCategory = onDeleteCategory;
    }

    /**
     * Add category data to the category list item
     *
     * @param category the category to add
     */
    public void addCategoryDataToCategoryListItem(Category category) {
        this.category = category;
        try {
            FXMLLoader loader = new FXMLLoader(getClass().getResource("/fxml/components/Category.fxml"));
            Node categoryNode = loader.load();

            CategoryController categoryController = loader.getController();
            categoryController.addCategoryDataToCategory(category);

            categoryListItemContainer.getChildren().addFirst(categoryNode);
        } catch (IOException e) {
            Logger.getLogger(CategoryListItemController.class.getName()).log(Level.SEVERE, "Error loading category fxml", e);
            throw new RuntimeException(e);
        }
    }
}
