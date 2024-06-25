package org.savingprivatenitti.controllers.widget;

import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.scene.Node;
import javafx.scene.layout.VBox;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.savingprivatenitti.TransactionType;
import javafx.scene.paint.Color;
import org.savingprivatenitti.models.Category;
import org.savingprivatenitti.models.Model;
import org.savingprivatenitti.models.Transaction;
import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.time.LocalDate;

import static org.mockito.Mockito.*;

public class RecentTransactionsWidgetControllerTest {

    @Test
    public void testUpdateRecentTransactions() throws Exception {
        Category category = new Category(1, "Test Category", Color.RED);
        // Create a mock of the Model class
        Model model = Mockito.mock(Model.class);

        // Define the behavior of the mock object
        Transaction transaction = new Transaction(1, TransactionType.INCOME, 200.0, LocalDate.now(), category); // Create a real Transaction or a mock
        when(model.getTransactions()).thenReturn(FXCollections.observableArrayList(transaction, transaction, transaction));

        // Use the mock object in your test
        RecentTransactionsWidgetController controller = new RecentTransactionsWidgetController(model);

        // Create a mock of VBox and set it as the value of recentTransactionListContainer
        VBox recentTransactionListContainerMock = Mockito.mock(VBox.class);
        Field recentTransactionListContainerField = RecentTransactionsWidgetController.class.getDeclaredField("recentTransactionListContainer");
        recentTransactionListContainerField.setAccessible(true);
        recentTransactionListContainerField.set(controller, recentTransactionListContainerMock);

        // Create a mock of ObservableList
        ObservableList<Node> observableListMock = Mockito.mock(ObservableList.class);

        // Define the behavior of getChildren()
        when(recentTransactionListContainerMock.getChildren()).thenReturn(observableListMock);

        // If the method is private, use reflection to access it
        Method method = RecentTransactionsWidgetController.class.getDeclaredMethod("updateRecentTransactions");

        // Make the method accessible
        method.setAccessible(true);

        // Call the method on the controller instance
        method.invoke(controller);

        // Verify that getChildren().clear() was called on the mock
        verify(recentTransactionListContainerMock.getChildren()).clear();

        // Verify that getChildren().add() was called on the mock for each transaction
        verify(recentTransactionListContainerMock.getChildren(), times(3)).add(any());

        // Verify that clear() was called on the mock
        verify(observableListMock).clear();

        // Verify that add() was called on the mock for each transaction
        verify(observableListMock, times(3)).add(any(Node.class));
    }
}