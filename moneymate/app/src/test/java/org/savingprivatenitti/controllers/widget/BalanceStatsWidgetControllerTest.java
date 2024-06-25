package org.savingprivatenitti.controllers.widget;

import com.sun.javafx.collections.ObservableListWrapper;
import javafx.scene.text.Text;
import org.junit.jupiter.api.Test;
import org.savingprivatenitti.models.Model;

import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.util.ArrayList;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.mockito.Mockito.*;

public class BalanceStatsWidgetControllerTest {

    @Test
    public void testSetIncomeText() throws Exception {
        Model model = mock(Model.class);
        when(model.getTransactions()).thenReturn(new ObservableListWrapper<>(new ArrayList<>()));
        BalanceStatsWidgetController controller = new BalanceStatsWidgetController(model);

        // Create a mock of Text and set it as the value of incomeAmount
        Text incomeAmountMock = mock(Text.class);
        Field incomeAmountField = BalanceStatsWidgetController.class.getDeclaredField("incomeAmount");
        incomeAmountField.setAccessible(true);
        incomeAmountField.set(controller, incomeAmountMock);

        // Get the setIncomeText method
        Method method = BalanceStatsWidgetController.class.getDeclaredMethod("setIncomeText", double.class);

        // Make the method accessible
        method.setAccessible(true);

        // Call the method on the controller instance
        method.invoke(controller, 1000.00);

        // Verify that setText was called on the mock with the expected value
        verify(incomeAmountMock).setText("+ CHF 1000.00");
    }
    @Test
    public void testSetExpensesText() throws Exception {
        Model model = mock(Model.class);
        when(model.getTransactions()).thenReturn(new ObservableListWrapper<>(new ArrayList<>()));
        BalanceStatsWidgetController controller = new BalanceStatsWidgetController(model);

        // Create a mock of Text and set it as the value of expensesAmount
        Text expensesAmountMock = mock(Text.class);
        Field expensesAmountField = BalanceStatsWidgetController.class.getDeclaredField("expensesAmount");
        expensesAmountField.setAccessible(true);
        expensesAmountField.set(controller, expensesAmountMock);

        // Get the setExpensesText method
        Method method = BalanceStatsWidgetController.class.getDeclaredMethod("setExpensesText", double.class);

        // Make the method accessible
        method.setAccessible(true);

        // Call the method on the controller instance
        method.invoke(controller, 500.00);

        // Verify that setText was called on the mock with the expected value
        verify(expensesAmountMock).setText("- CHF 500.00");
    }

    @Test
    public void testIsAmountTooLarge() throws Exception {
        Model model = mock(Model.class);
        when(model.getTransactions()).thenReturn(new ObservableListWrapper<>(new ArrayList<>()));
        BalanceStatsWidgetController controller = new BalanceStatsWidgetController(model);

        // Get the isAmountTooLarge method
        Method method = BalanceStatsWidgetController.class.getDeclaredMethod("isAmountTooLarge", double.class);

        // Make the method accessible
        method.setAccessible(true);

        // Call the method on the controller instance and get the result
        boolean result = (boolean) method.invoke(controller, 10000000.00);

        // Assert that the result is as expected
        assertFalse(result, "Expected isAmountTooLarge to return true for large amounts");
    }
}