package org.savingprivatenitti.controllers.primitive;

import javafx.fxml.FXML;
import javafx.scene.layout.Pane;
import javafx.scene.text.Font;
import javafx.scene.text.Text;
import org.savingprivatenitti.TransactionType;
import org.savingprivatenitti.models.Category;
import org.savingprivatenitti.models.Transaction;
import org.savingprivatenitti.utils.ColorConverter;
import org.savingprivatenitti.utils.DateFormatter;
import org.savingprivatenitti.utils.TextFormatter;

import java.time.LocalDate;

public class TransactionController {

    @FXML
    private Pane transactionPane;

    @FXML
    private Text transactionAmount;

    @FXML
    private Text transactionDate;

    @FXML
    private Text transactionCategory;


    /**
     * Add transaction data to the transaction
     * @param transaction the transaction to add
     */
    public void addTransactionDataToTransaction(Transaction transaction) {
        setTransactionAmount(transaction.type(), transaction.amount());
        setTransactionDate(transaction.date());
        setTransactionCategory(transaction.category());
        applyBorderColor(transaction.type());
    }

    private void applyTextColor(TransactionType transactionType) {
        switch (transactionType) {
            case INCOME:
                transactionAmount.setStyle("-fx-fill: #99DB69;");
                break;
            case EXPENSE:
                transactionAmount.setStyle("-fx-fill: #DF5F5F;");
                break;
        }
    }

    private void applyBorderColor(TransactionType transactionType) {
        switch (transactionType) {
            case INCOME:
                transactionPane.setStyle("-fx-border-color: #99DB69;");
                break;
            case EXPENSE:
                transactionPane.setStyle("-fx-border-color: #DF5F5F;");
                break;
        }
    }

    private void formatTransactionAmountText(TransactionType transactionType) {
        switch (transactionType) {
            case INCOME:
                transactionAmount.setText("+" + transactionAmount.getText() + " CHF");
                break;
            case EXPENSE:
                transactionAmount.setText("-" + transactionAmount.getText() + " CHF");
                break;
        }
    }

    private void setTransactionAmount(TransactionType transactionType, Double amount) {
        String amountText = String.format("%.2f", amount);
        amountText = TextFormatter.shortenTextToFit(amountText, 80, new Font("Source Sans Pro Bold", 20.0));
        transactionAmount.setText(amountText);
        formatTransactionAmountText(transactionType);
        applyTextColor(transactionType);
    }

    private void setTransactionDate(LocalDate date) {
        String formattedDate = date.format(DateFormatter.DATE_FORMATTER);
        transactionDate.setText(formattedDate);
    }

    private void setTransactionCategory(Category category) {
        transactionCategory.setText(TextFormatter.shortenTextToFit(category.label(), 120, new Font("Source Sans Pro Bold", 18.0)));
        transactionCategory.setStyle("-fx-fill: " + ColorConverter.toHex(category.color()) + ";");
    }

}
