package org.savingprivatenitti.controllers.widget;

import javafx.collections.ListChangeListener;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.Group;
import javafx.scene.Node;
import javafx.scene.chart.CategoryAxis;
import javafx.scene.chart.NumberAxis;
import javafx.scene.chart.StackedBarChart;
import javafx.scene.chart.XYChart;
import javafx.scene.text.Text;
import org.savingprivatenitti.TransactionType;
import org.savingprivatenitti.models.Model;
import org.savingprivatenitti.models.Transaction;
import org.savingprivatenitti.utils.DateFormatter;

import java.net.URL;
import java.time.DayOfWeek;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.time.temporal.TemporalAdjusters;
import java.util.Arrays;
import java.util.Map;
import java.util.ResourceBundle;
import java.util.stream.Collectors;

public class WeeklySavingsOverviewWidgetController extends WidgetController implements Initializable {

    @FXML
    private Group widgetGroup;

    @FXML
    private StackedBarChart<String, Number> weeklySavingsStackedBarChart;

    @FXML
    private CategoryAxis weekdayAxis;

    @FXML
    private NumberAxis amountAxis;

    @FXML
    private Text startOfWeekDateText;

    /**
     * Create a new WeeklySavingsOverviewWidgetController
     * @param model the model
     */
    public WeeklySavingsOverviewWidgetController(Model model) {
        super(model);
    }

    @Override
    public void initialize(URL location, ResourceBundle resources) {
        model.getTransactions().addListener((ListChangeListener<Transaction>) change -> updateWeeklySavingsOverview());
        updateWeeklySavingsOverview();
        scalableNode = widgetGroup;
        applyScaleEffect();
    }

    private void updateWeeklySavingsOverview() {
        clearWeeklySavingsOverview();

        LocalDate now = LocalDate.now();
        LocalDate monday = now.with(TemporalAdjusters.previousOrSame(DayOfWeek.MONDAY));
        LocalDate sunday = now.with(TemporalAdjusters.nextOrSame(DayOfWeek.SUNDAY));
//        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("dd-MM-yyyy");
        DateTimeFormatter formatter = DateFormatter.DATE_FORMATTER;

        startOfWeekDateText.setText(monday.format(formatter) + " - " + sunday.format(formatter));
        Map<LocalDate, Map<TransactionType, Double>> transactionsByDateAndType = groupTransactionsByDateAndType(monday, sunday, formatter);

        XYChart.Series<String, Number> incomeSeries = createSeries("Income", transactionsByDateAndType, monday, TransactionType.INCOME);
        XYChart.Series<String, Number> expenseSeries = createSeries("Expense", transactionsByDateAndType, monday, TransactionType.EXPENSE);

        weeklySavingsStackedBarChart.getData().addAll(Arrays.asList(incomeSeries, expenseSeries));

        applyCssClassesToSeries(incomeSeries, "income");
        applyCssClassesToSeries(expenseSeries, "expense");

        weeklySavingsStackedBarChart.layout();
    }

    private Map<LocalDate, Map<TransactionType, Double>> groupTransactionsByDateAndType(LocalDate monday, LocalDate sunday, DateTimeFormatter formatter) {
        return model.getTransactions().stream()
                .filter(transaction -> {
                    LocalDate date = LocalDate.parse(transaction.getDate(), formatter);
                    return !date.isBefore(monday) && !date.isAfter(sunday);
                })
                .collect(Collectors.groupingBy(
                        transaction -> LocalDate.parse(transaction.getDate(), formatter),
                        Collectors.groupingBy(
                                Transaction::type,
                                Collectors.summingDouble(Transaction::amount)
                        )
                ));
    }

    private XYChart.Series<String, Number> createSeries(String name, Map<LocalDate, Map<TransactionType, Double>> transactionsByDateAndType, LocalDate monday, TransactionType type) {
        XYChart.Series<String, Number> series = new XYChart.Series<>();
        series.setName(name);

        for (int i = 0; i < 7; i++) {
            LocalDate date = monday.plusDays(i);
            Map<TransactionType, Double> transactionsByType = transactionsByDateAndType.getOrDefault(date, Map.of());

            double income = transactionsByType.getOrDefault(TransactionType.INCOME, 0.0);
            double expense = transactionsByType.getOrDefault(TransactionType.EXPENSE, 0.0);

            double netIncome = income - expense;

            if (type == TransactionType.INCOME) {
                series.getData().add(new XYChart.Data<>(date.getDayOfWeek().toString(), netIncome > 0 ? netIncome : 0));
            } else {
                series.getData().add(new XYChart.Data<>(date.getDayOfWeek().toString(), expense));
            }
        }

        return series;
    }

    private void applyCssClassesToSeries(XYChart.Series<String, Number> series, String cssClass) {
        for (XYChart.Data<String, Number> data : series.getData()) {
            Node node = data.getNode();
            node.getStyleClass().add(cssClass);
        }
    }

    private void clearWeeklySavingsOverview() {
        weeklySavingsStackedBarChart.getData().clear();
    }

}