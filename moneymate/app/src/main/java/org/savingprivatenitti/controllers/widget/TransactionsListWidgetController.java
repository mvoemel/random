package org.savingprivatenitti.controllers.widget;

import javafx.collections.ListChangeListener;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.fxml.Initializable;
import javafx.scene.Group;
import javafx.scene.Node;
import javafx.scene.control.ScrollPane;
import javafx.scene.layout.VBox;
import org.savingprivatenitti.controllers.listitem.TransactionListItemController;
import org.savingprivatenitti.models.Model;
import org.savingprivatenitti.models.Transaction;

import java.io.IOException;
import java.net.URL;
import java.util.ResourceBundle;
import java.util.logging.Level;
import java.util.logging.Logger;

public class TransactionsListWidgetController extends WidgetController implements Initializable {

    @FXML
    private Group widgetGroup;

    @FXML
    private VBox transactionsListContainer;

    @FXML
    private ScrollPane transactionsListScrollPane;

    /**
     * Create a new TransactionsListWidgetController
     * @param model the model
     */
    public TransactionsListWidgetController(Model model) {
        super(model);
    }

    @Override
    public void initialize(URL location, ResourceBundle resources) {
        model.getTransactions().addListener((ListChangeListener<Transaction>) change -> updateTransactionsList());
        updateTransactionsList();
        scalableNode = widgetGroup;
        applyScaleEffect();
    }

    private void updateTransactionsList() {
        transactionsListContainer.getChildren().clear(); // Clear the existing transactions
        model.getTransactions().reversed().forEach(transaction -> {
            try {
                // Load the transaction item FXML file
                FXMLLoader loader = new FXMLLoader(getClass().getResource("/fxml/components/TransactionListItem.fxml"));
                Node transactionItem = loader.load();
                // Get the controller of the transaction item and set the transaction
                TransactionListItemController transactionListItemController = loader.getController();
                transactionListItemController.setOnDeleteTransaction(model::removeTransaction);
                transactionListItemController.addTransactionDataToTransactionItem(transaction);

                // Add the transaction item to the transactions container
                transactionsListContainer.getChildren().add(transactionItem);
            } catch (IOException e) {
                Logger.getLogger(TransactionsListWidgetController.class.getName()).log(Level.WARNING, "Failed to load TransactionListItem fxml");
            }
        });
        transactionsListScrollPane.requestLayout();
    }

}