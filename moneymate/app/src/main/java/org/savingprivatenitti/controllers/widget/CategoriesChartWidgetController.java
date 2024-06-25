package org.savingprivatenitti.controllers.widget;

import javafx.collections.ListChangeListener;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.Group;
import javafx.scene.chart.PieChart;
import org.savingprivatenitti.TransactionType;
import org.savingprivatenitti.models.Model;
import org.savingprivatenitti.models.Transaction;
import org.savingprivatenitti.utils.ColorConverter;

import java.net.URL;
import java.time.DayOfWeek;
import java.time.LocalDate;
import java.util.List;
import java.util.Map;
import java.util.ResourceBundle;
import java.util.stream.Collectors;

public class CategoriesChartWidgetController extends WidgetController implements Initializable {

    @FXML
    private Group widgetGroup;

    @FXML
    private PieChart categoriesPieChart;

    /**
     * Create a new CategoriesChartWidgetController
     * @param model the model
     */
    public CategoriesChartWidgetController(Model model) {
        super(model);
    }

    @Override
    public void initialize(URL location, ResourceBundle resources) {
        model.getTransactions().addListener((ListChangeListener<Transaction>) change -> updateCategoriesPieChart());
        updateCategoriesPieChart();
        scalableNode = widgetGroup;
        applyScaleEffect();
    }

    private void updateCategoriesPieChart() {
        clearCategoriesPieChart();

        LocalDate startOfWeek = LocalDate.now().with(DayOfWeek.MONDAY);
        LocalDate endOfWeek = LocalDate.now().with(DayOfWeek.SUNDAY);

        List<Transaction> transactions = model.getTransactions();

        Map<String, List<Transaction>> categoryTransactions = transactions.stream()
                .filter(transaction -> transaction.type() == TransactionType.EXPENSE)
                .filter(transaction -> !transaction.date().isBefore(startOfWeek) && !transaction.date().isAfter(endOfWeek))
                .collect(Collectors.groupingBy(transaction -> transaction.category().label()));

        for (Map.Entry<String, List<Transaction>> entry : categoryTransactions.entrySet()) {
            double sum = entry.getValue().stream().mapToDouble(Transaction::amount).sum();
            PieChart.Data slice = new PieChart.Data(entry.getKey(), sum);
            categoriesPieChart.getData().add(slice);

            // Set the color of the slice
            String color = ColorConverter.toHex(entry.getValue().getFirst().category().color());
            slice.getNode().setStyle("-fx-pie-color: " + color + ";");
        }
        categoriesPieChart.setLegendVisible(false);
    }

    private void clearCategoriesPieChart() {
        categoriesPieChart.getData().clear();
    }
}