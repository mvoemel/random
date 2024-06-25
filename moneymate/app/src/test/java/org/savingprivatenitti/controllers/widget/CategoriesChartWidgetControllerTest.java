package org.savingprivatenitti.controllers.widget;

import com.sun.javafx.collections.ObservableListWrapper;
import javafx.collections.FXCollections;
import javafx.scene.chart.PieChart;
import org.junit.jupiter.api.Test;
import org.savingprivatenitti.models.Model;

import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.util.ArrayList;

import static org.mockito.Mockito.*;

public class CategoriesChartWidgetControllerTest {

    @Test
    public void testUpdateCategoriesPieChart() throws Exception {
        Model model = mock(Model.class);
        when(model.getTransactions()).thenReturn(new ObservableListWrapper<>(new ArrayList<>()));
        CategoriesChartWidgetController controller = new CategoriesChartWidgetController(model);

        // Create a mock of PieChart and set it as the value of categoriesPieChart
        PieChart categoriesPieChartMock = mock(PieChart.class);
        Field categoriesPieChartField = CategoriesChartWidgetController.class.getDeclaredField("categoriesPieChart");
        categoriesPieChartField.setAccessible(true);
        categoriesPieChartField.set(controller, categoriesPieChartMock);

        // Define the behavior of getData()
        when(categoriesPieChartMock.getData()).thenReturn(FXCollections.observableArrayList());

        // Get the updateCategoriesPieChart method
        Method method = CategoriesChartWidgetController.class.getDeclaredMethod("updateCategoriesPieChart");

        // Make the method accessible
        method.setAccessible(true);

        // Call the method on the controller instance
        method.invoke(controller);

        // Verify that getData was called on the mock
        verify(categoriesPieChartMock).getData();
    }
}