package org.savingprivatenitti.controllers.widget;

import javafx.collections.ListChangeListener;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.fxml.Initializable;
import javafx.scene.Group;
import javafx.scene.Node;
import javafx.scene.layout.VBox;
import org.savingprivatenitti.controllers.primitive.TransactionController;
import org.savingprivatenitti.models.Model;
import org.savingprivatenitti.models.Transaction;

import java.io.IOException;
import java.net.URL;
import java.util.Comparator;
import java.util.ResourceBundle;
import java.util.logging.Level;
import java.util.logging.Logger;

public class RecentTransactionsWidgetController extends WidgetController implements Initializable {

    @FXML
    private Group widgetGroup;

    @FXML
    private VBox recentTransactionListContainer;

    /**
     * Create a new RecentTransactionsWidgetController
     * @param model the model
     */
    public RecentTransactionsWidgetController(Model model) {
        super(model);
    }

    @Override
    public void initialize(URL location, ResourceBundle resources) {
        model.getTransactions().addListener((ListChangeListener<Transaction>) change -> updateRecentTransactions());
        updateRecentTransactions();
        scalableNode = widgetGroup;
        applyScaleEffect();
    }

    private void updateRecentTransactions() {
        recentTransactionListContainer.getChildren().clear(); // Clear the existing transactions
        model.getTransactions().stream()
                .sorted(Comparator.comparing(Transaction::date).reversed()) // Sort the transactions by date in descending order
                .limit(8) // Get the 8 most recent transactions
                .forEach(transaction -> {
                    try {
                        // Load the transaction item FXML file
                        FXMLLoader loader = new FXMLLoader(getClass().getResource("/fxml/components/Transaction.fxml"));
                        Node transactionItem = loader.load();

                        // Get the controller of the transaction item and set the transaction
                        TransactionController controller = loader.getController();
                        controller.addTransactionDataToTransaction(transaction);

                        // Add the transaction item to the transactions container
                        recentTransactionListContainer.getChildren().add(transactionItem);
                    } catch (IOException e) {
                        Logger.getLogger(RecentTransactionsWidgetController.class.getName()).log(Level.WARNING, "Failed to load Transaction fxml");
                    }
                });
    }
}