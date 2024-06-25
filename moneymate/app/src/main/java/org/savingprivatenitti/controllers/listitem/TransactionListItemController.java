package org.savingprivatenitti.controllers.listitem;

import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Node;
import javafx.scene.control.Button;
import javafx.scene.layout.HBox;
import org.savingprivatenitti.controllers.primitive.TransactionController;
import org.savingprivatenitti.models.Transaction;

import java.io.IOException;
import java.util.function.Consumer;
import java.util.logging.Level;
import java.util.logging.Logger;

public class TransactionListItemController {

    @FXML
    private HBox transactionListItemContainer;

    @FXML
    private Button transactionListItemDelete;

    private Consumer<Transaction> onDeleteTransaction;

    private Transaction transaction;

    /**
     * Handle the event when the delete button is clicked
     */
    @FXML
    public void onTransactionDeleteButtonClicked() {
        if (onDeleteTransaction != null) {
            onDeleteTransaction.accept(transaction);
        } else {
            Logger.getLogger(TransactionListItemController.class.getName()).log(Level.SEVERE, "Error trying to delete transaction: onDeleteTransaction consumer is not set");
            throw new RuntimeException("onDeleteTransaction consumer is not set");
        }
    }

    /**
     * Set the consumer for the onDeleteTransaction event
     * @param onDeleteTransaction the consumer for the onDeleteTransaction event
     */
    public void setOnDeleteTransaction(Consumer<Transaction> onDeleteTransaction) {
        this.onDeleteTransaction = onDeleteTransaction;
    }

    /**
     * Add transaction data to the transaction list item
     * @param transaction the transaction (data) to add to the transactionItem
     */
    public void addTransactionDataToTransactionItem(Transaction transaction) {
        this.transaction = transaction;
        try {
            FXMLLoader loader = new FXMLLoader(getClass().getResource("/fxml/components/TransactionWide.fxml"));
            Node transactionNode = loader.load();

            TransactionController transactionController = loader.getController();
            transactionController.addTransactionDataToTransaction(transaction);

            transactionListItemContainer.getChildren().addFirst(transactionNode);
        } catch (IOException e) {
            Logger.getLogger(TransactionListItemController.class.getName()).log(Level.SEVERE, "Error loading TransactionWide fxml", e);
            throw new RuntimeException(e);
        }
    }

}
