package org.savingprivatenitti.controllers.widget;

import javafx.collections.ListChangeListener;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.Group;
import javafx.scene.control.Label;
import javafx.scene.text.Text;
import org.savingprivatenitti.TransactionType;
import org.savingprivatenitti.models.Model;
import org.savingprivatenitti.models.Transaction;

import java.net.URL;
import java.time.DayOfWeek;
import java.time.LocalDate;
import java.util.ResourceBundle;


public class BalanceStatsWidgetController extends WidgetController implements Initializable {

    @FXML
    private Group widgetGroup;

    @FXML
    private Label incomeLabel;

    @FXML
    private Label expensesLabel;

    @FXML
    private Text incomeAmount;

    @FXML
    private Text expensesAmount;

    /**
     * Create a new BalanceStatsWidgetController
     * @param model the model
     */
    public BalanceStatsWidgetController(Model model) {
        super(model);
    }

    @Override
    public void initialize(URL location, ResourceBundle resources) {
        model.getTransactions().addListener((ListChangeListener<Transaction>) change -> updateStats());
        updateStats();
        scalableNode = widgetGroup;
        applyScaleEffect();
    }

    private void updateStats() {
        double income = 0.0;
        double expenses = 0.0;

        LocalDate currentDate = LocalDate.now();

        LocalDate startOfWeek = currentDate.with(DayOfWeek.MONDAY);
        LocalDate endOfWeek = currentDate.with(DayOfWeek.SUNDAY);

        for (Transaction transaction : model.getTransactions()) {
            // Check if the transaction date is within the current week
            if (!transaction.date().isBefore(startOfWeek) && !transaction.date().isAfter(endOfWeek)) {
                if (transaction.type() == TransactionType.INCOME) {
                    income += transaction.amount();
                } else if (transaction.type() == TransactionType.EXPENSE) {
                    expenses += transaction.amount();
                }
            }
        }
        setIncomeText(income);
        setExpensesText(expenses);
    }

    private void setExpensesText(double expenses) {
        if (isAmountTooLarge(expenses)) {
            expensesAmount.setText("< CHF -9999999");
        } else {
            expensesAmount.setText(String.format("- CHF %.2f", expenses));
        }
    }

    private void setIncomeText(double income) {
        if (isAmountTooLarge(income)) {
            incomeAmount.setText("> CHF +9999999");
        } else {
            incomeAmount.setText(String.format("+ CHF %.2f", income));
        }
    }

    private boolean isAmountTooLarge(double amount) {
        return String.format("%.2f", amount).length() > 12;
    }

}