package org.savingprivatenitti.controllers.models;

import javafx.scene.paint.Color;
import org.junit.jupiter.api.Test;
import org.savingprivatenitti.TransactionType;
import org.savingprivatenitti.models.Transaction;
import org.savingprivatenitti.models.Category;
import java.time.LocalDate;

import static org.junit.jupiter.api.Assertions.*;

public class TransactionTest {

    private final Category cat = new Category(1, "Food", Color.RED);

    @Test
    public void testGetDate() {
        LocalDate date = LocalDate.of(2022, 1, 1); // January 1, 2022
        Transaction transaction = new Transaction(1, TransactionType.INCOME, 100.0, date, cat);

        String expected = "01.01.2022";
        assertEquals(expected, transaction.getDate());
    }

    @Test
    public void testRecordConstructor() {
        LocalDate date = LocalDate.of(2022, 1, 1); // January 1, 2022
        Transaction transaction = new Transaction(1, TransactionType.INCOME, 100.0, date, cat);

        assertEquals(1, transaction.id());
        assertEquals(TransactionType.INCOME, transaction.type());
        assertEquals(100.0, transaction.amount());
        assertEquals(date, transaction.date());
        assertEquals(cat, transaction.category());
    }
}