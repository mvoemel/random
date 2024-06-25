package org.savingprivatenitti.controllers.widget;

import javafx.collections.SetChangeListener;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.fxml.Initializable;
import javafx.scene.Group;
import javafx.scene.Node;
import javafx.scene.control.ScrollPane;
import javafx.scene.layout.VBox;
import org.savingprivatenitti.controllers.listitem.CategoryListItemController;
import org.savingprivatenitti.models.Category;
import org.savingprivatenitti.models.Model;

import java.io.IOException;
import java.net.URL;
import java.util.ResourceBundle;
import java.util.logging.Level;
import java.util.logging.Logger;

public class CategoriesListWidgetController extends WidgetController implements Initializable {

    @FXML
    private Group widgetGroup;

    @FXML
    private VBox categoriesListContainer;

    @FXML
    private ScrollPane categoriesListScrollPane;

    /**
     * Create a new CategoriesListWidgetController
     * @param model the model
     */
    public CategoriesListWidgetController(Model model) {
        super(model);
    }

    @Override
    public void initialize(URL location, ResourceBundle resources) {
        model.getCategories().addListener((SetChangeListener<Category>) change -> updateCategoriesList());
        updateCategoriesList();
        scalableNode = widgetGroup;
        applyScaleEffect();
    }

    private void updateCategoriesList() {
        categoriesListContainer.getChildren().clear(); // Clear the existing categories
        model.getCategories().forEach(category -> {
            try {
                FXMLLoader loader = new FXMLLoader(getClass().getResource("/fxml/components/CategoryListItem.fxml"));
                Node categoryListItem = loader.load();

                CategoryListItemController categoryListItemController = loader.getController();
                categoryListItemController.setOnDeleteCategory(model::removeCategory);
                categoryListItemController.addCategoryDataToCategoryListItem(category);

                categoriesListContainer.getChildren().add(categoryListItem);
            } catch (IOException e) {
                Logger.getLogger(CategoriesListWidgetController.class.getName()).log(Level.WARNING, "Failed to load CategoryListItem fxml");
                throw new RuntimeException(e);
            }
        });
        categoriesListScrollPane.requestLayout();
    }
}