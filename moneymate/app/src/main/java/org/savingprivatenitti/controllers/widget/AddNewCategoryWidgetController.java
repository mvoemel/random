package org.savingprivatenitti.controllers.widget;

import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.Group;
import javafx.scene.control.Button;
import javafx.scene.control.ColorPicker;
import javafx.scene.control.TextField;
import javafx.scene.paint.Color;
import org.savingprivatenitti.controllers.modal.Modal;
import org.savingprivatenitti.models.Model;

import java.net.URL;
import java.util.ResourceBundle;
import java.util.logging.Level;
import java.util.logging.Logger;

public class AddNewCategoryWidgetController extends WidgetController implements Initializable {

    @FXML
    private Group widgetGroup;

    @FXML
    private Button addCategoryButton;

    @FXML
    private ColorPicker categoryColorPicker;

    @FXML
    private TextField categoryLabel;

    /**
     * Handle the event when the add category button is clicked
     */
    @FXML
    public void onAddCategoryButtonClicked() {
        try {
            String label = categoryLabel.getText();
            Color color = categoryColorPicker.getValue();

            if (categoryAlreadyExists(label, color)) {
                throw new CategoryAlreadyExistsException("");
            }

            if (label.isEmpty()) {
                throw new CategoryMissingLabelException("");
            }

            model.addCategory(label, color);
            clearFormElements();
        } catch (CategoryAlreadyExistsException e) {
            Logger.getLogger(AddNewCategoryWidgetController.class.getName()).log(Level.WARNING, "Category already exists");
            showCategoryAlreadyExistsErrorModal();
        } catch (CategoryMissingLabelException e) {
            Logger.getLogger(AddNewCategoryWidgetController.class.getName()).log(Level.WARNING, "Category is empty");
            showMissingCategoryLabelErrorModal();
        }
    }

    /**
     * Create a new AddNewCategoryWidgetController
     * @param model the model
     */
    public AddNewCategoryWidgetController(Model model) {
        super(model);
    }

    @Override
    public void initialize(URL location, ResourceBundle resources) {
        categoryColorPicker.getStyleClass().add("button");
        scalableNode = widgetGroup;
        applyScaleEffect();
    }

    private void showCategoryAlreadyExistsErrorModal() {
        String message = "The category you are trying to add already exists. Please enter a unique category label.";
        Modal.showMessage(message);
    }

    private void showMissingCategoryLabelErrorModal() {
        String message = "Please enter a category label.";
        Modal.showMessage(message);
    }

    private boolean categoryAlreadyExists(String label, Color color) {
        return model.getCategories().stream().anyMatch(category -> category.label().equals(label) && category.color().equals(color));
    }

    private void clearFormElements() {
        categoryLabel.clear();
        categoryColorPicker.setValue(Color.WHITE);
    }

}