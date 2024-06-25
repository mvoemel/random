package org.savingprivatenitti.controllers.widget;

import javafx.collections.SetChangeListener;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.Group;
import javafx.scene.control.Button;
import javafx.scene.control.ChoiceBox;
import javafx.scene.control.DatePicker;
import javafx.scene.control.TextField;
import javafx.util.StringConverter;
import org.savingprivatenitti.TransactionType;
import org.savingprivatenitti.controllers.modal.Modal;
import org.savingprivatenitti.models.Category;
import org.savingprivatenitti.models.Model;
import org.savingprivatenitti.utils.DateFormatter;

import java.net.URL;
import java.time.LocalDate;
import java.util.List;
import java.util.ResourceBundle;
import java.util.logging.Level;
import java.util.logging.Logger;

public class AddNewEntryWidgetController extends WidgetController implements Initializable {

    @FXML
    private Group widgetGroup;

    @FXML
    private ChoiceBox<String> transactionTypeChoiceBox;

    @FXML
    private TextField amountTextField;

    @FXML
    private ChoiceBox<String> categoryChoiceBox;

    @FXML
    private DatePicker transactionDatePicker;

    @FXML
    private Button addNewEntryButton;

    /**
     * Create a new AddNewEntryWidgetController
     * @param model the model
     */
    public AddNewEntryWidgetController(Model model) {
        super(model);
    }

    /**
     * Handle the event when the add new entry button is clicked
     */
    @FXML
    public void onAddNewEntryButtonClicked() {
        try {
            TransactionType transactionType = getTransactionType();
            double amount = getTransactionAmount();
            Category category = getTransactionCategory();
            LocalDate date = getTransactionDate();
            model.addTransaction(transactionType, amount, date, category);
            clearFormElements();
        } catch (NumberFormatException | NullPointerException e) {
            showInvalidTransactionErrorModal();
        }
    }

    @Override
    public void initialize(URL location, ResourceBundle resources) {
        model.getCategories().addListener((SetChangeListener<Category>) change -> updateCategories());
        clearChoiceBoxes();
        initializeTransactionTypeChoiceBox();
        initializeCategoryChoiceBox();
        setupDatePickerFormat();
        scalableNode = widgetGroup;
        applyScaleEffect();
    }

    private TransactionType getTransactionType() {
        return TransactionType.valueOf(transactionTypeChoiceBox.getValue());
    }

    private double getTransactionAmount() {
        return Double.parseDouble(amountTextField.getText());
    }

    private Category getTransactionCategory() {
        Category category = model.getCategoryByLabel(categoryChoiceBox.getValue());
        if (category == null) {
            Logger.getLogger(AddNewEntryWidgetController.class.getName()).log(Level.WARNING, "Category was null");
            throw new NullPointerException();
        } else {
            return category;
        }
    }

    private LocalDate getTransactionDate() {
        LocalDate transactionDate = transactionDatePicker.getValue();
        System.out.println("Transaction Date: " + transactionDate);
        if (transactionDate == null) {
            Logger.getLogger(AddNewEntryWidgetController.class.getName()).log(Level.WARNING, "TransactionDate was null");
            throw new NullPointerException();
        } else {
            return transactionDate;
        }
    }

    private void initializeTransactionTypeChoiceBox() {
        transactionTypeChoiceBox.getItems().addAll(TransactionType.INCOME.toString(), TransactionType.EXPENSE.toString());
    }

    private void initializeCategoryChoiceBox() {
        categoryChoiceBox.getItems().addAll(getCategorieNames());
    }

    private void showInvalidTransactionErrorModal() {
        String message = "Please make sure to fill out all fields correctly.";
        Modal.showMessage(message);
    }

    private void updateCategories() {
        categoryChoiceBox.getItems().clear();
        categoryChoiceBox.getItems().addAll(getCategorieNames());
    }

    private List<String> getCategorieNames() {
        return model.getCategories().stream().map(Category::label).toList();
    }

    private void setupDatePickerFormat() {
        StringConverter<LocalDate> converter = new StringConverter<>() {

            @Override
            public String toString(LocalDate date) {
                if (date != null) {
                    return DateFormatter.DATE_FORMATTER.format(date);
                } else {
                    return "";
                }
            }

            @Override
            public LocalDate fromString(String string) {
                if (string != null && !string.isEmpty()) {
                    return LocalDate.parse(string, DateFormatter.DATE_FORMATTER);
                } else {
                    return null;
                }
            }
        };
        transactionDatePicker.setConverter(converter);
    }

    private void clearFormElements() {
        transactionTypeChoiceBox.setValue(null);
        amountTextField.clear();
        categoryChoiceBox.setValue(null);
        transactionDatePicker.setValue(null);
    }

    private void clearChoiceBoxes() {
        transactionTypeChoiceBox.getItems().clear();
        categoryChoiceBox.getItems().clear();
    }
}