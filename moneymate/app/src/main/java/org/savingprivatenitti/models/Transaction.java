package org.savingprivatenitti.models;

import org.savingprivatenitti.TransactionType;
import org.savingprivatenitti.utils.DateFormatter;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;

/**
 * A record representing a transaction
 *
 * @param id       the id of transition
 * @param type     the type of transaction
 * @param amount   the amount of the transaction
 * @param date     the date of the transaction
 * @param category the category of the transaction
 */
public record Transaction(int id, TransactionType type, double amount, LocalDate date, Category category) {
//    private static final DateTimeFormatter formatter = DateTimeFormatter.ofPattern("dd-MM-yyyy");


    public String getDate() {
        return date.format(DateFormatter.DATE_FORMATTER);
    }
}
