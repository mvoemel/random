package org.savingprivatenitti.models;

import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.collections.ObservableSet;
import javafx.scene.paint.Color;
import org.mindrot.jbcrypt.BCrypt;
import org.savingprivatenitti.TransactionType;

import java.sql.SQLException;
import java.time.LocalDate;
import java.util.List;
import java.util.Set;
import java.util.TreeSet;
import java.util.logging.Level;
import java.util.logging.Logger;

public class Model {

    private final DatabaseManager databaseManager;

    private final ObservableList<Transaction> transactions;
    private final ObservableSet<Category> categories;

    private User currentUser;

    /**
     * Constructor of the Model class.
     */
    public Model() {
        try {
            this.databaseManager = new DatabaseManager();
            this.transactions = FXCollections.observableArrayList();
            this.categories = FXCollections.observableSet(new TreeSet<>());
        } catch (Exception e) {
            Logger.getLogger(Model.class.getName()).log(Level.SEVERE, "Error setting up Model: " + e.getMessage());
            throw new RuntimeException(e);
        }
    }

    /**
     * Initializes the model with the user's transactions and categories.
     * @param userId the ID of the user whose transactions and categories to initialize with
     * @throws SQLException if there is a problem connecting to the database
     * @throws RuntimeException if the initialization process fails
     */
    private void init(int userId) throws SQLException, RuntimeException {
        List<Transaction> transactions = databaseManager.getAllTransactions(userId);
        Set<Category> categories = databaseManager.getAllCategories(userId);
        boolean initTransactionsSuccess = this.transactions.addAll(transactions);
        boolean initCategoriesSuccess = this.categories.addAll(categories);

        if ((!initTransactionsSuccess || !initCategoriesSuccess) && !transactions.isEmpty() && !categories.isEmpty()) {
            throw new RuntimeException("Unable to initialize model (transactionsSuccess: " + initTransactionsSuccess + ", categoriesSuccess: " + initCategoriesSuccess + ")");
        }
    }

    /**
     * Logs the user into the application.
     * @param loginToken the token containing the user's username and password
     * @return true if the login is successful, false otherwise
     * @throws RuntimeException if the login process fails
     */
    public boolean login(LoginToken loginToken) {
        try {
            this.currentUser = databaseManager.getUserByUsername(loginToken.username());
            if (this.currentUser == null) {
                throw new UnableToFindUserException("Unable to find user with username: " + loginToken.username());
            }

            if (!this.passwordsMatch(loginToken.password(), this.currentUser.password())) {
                throw new WrongPasswordException("Incorrect password for user: " + loginToken.username());
            }

            init(this.currentUser.id());
        } catch (UnableToFindUserException | WrongPasswordException e) {
            Logger.getLogger(Model.class.getName()).log(Level.SEVERE, e.getMessage());
            return false;
        } catch (SQLException | RuntimeException e) {
            Logger.getLogger(Model.class.getName()).log(Level.SEVERE, "Error login: " + e.getMessage());
            return false;
        }
        return true;
    }

    /**
     * Logs the user out of the application.
     * @return true if the logout is successful, false otherwise
     * @throws RuntimeException if the logout process fails
     */
    public boolean logout() {
        try {
            this.currentUser = null;
            this.transactions.clear();
            this.categories.clear();
        } catch (RuntimeException e) {
            return false;
        }
        return  true;
    }

    /**
     * Registers a new user in the application.
     * @param signUpToken the token containing the user's username, email, and password
     * @return true if the registration is successful, false otherwise
     * @throws RuntimeException if the registration process fails
     */
    public boolean signUp(SignUpToken signUpToken) {
        try {
            int newUserId = databaseManager.addNewUser(signUpToken.username(), signUpToken.email(), hashPassword(signUpToken.password()));
            Logger.getLogger(Model.class.getName()).log(Level.FINE, "New user id: " + newUserId);
            this.currentUser = databaseManager.getUserById(newUserId);

            init(this.currentUser.id());
        } catch (SQLException | RuntimeException e) {
            return false;
        }
        return true;
    }


    /**
     * Get the list of transactions
     * @return the list of transactions
     */
    public ObservableList<Transaction> getTransactions() {
        return transactions;
    }

    /**
     * Get the set of categories
     * @return the set of categories
     */
    public ObservableSet<Category> getCategories() {
        return categories;
    }


    /**
     * Add a transaction to the list of transactions
     * @param transactionType the type of the transaction
     * @param amount the amount of the transaction
     * @param date the date of the transaction
     * @param category the category of the transaction
     */
    public void addTransaction(TransactionType transactionType, double amount, LocalDate date, Category category) {
        int newTransactionId;
        try {
            newTransactionId = databaseManager.addTransaction(this.currentUser.id(), transactionType, amount, date, category);
        } catch (SQLException e) {
            Logger.getLogger(Model.class.getName()).log(Level.SEVERE, e.getMessage());
            throw new RuntimeException(e);
        }

        Transaction newTransaction = new Transaction(newTransactionId, transactionType, amount, date, category);
        transactions.add(newTransaction);
    }

    /**
     * Add a category to the set of categories
     * @param label the label of the category
     * @param color the color of the category
     */
    public void addCategory(String label, Color color) {
        int newCategoryId;
        try {
            newCategoryId = databaseManager.addCategory(this.currentUser.id(), label, color);
        } catch (SQLException e) {
            Logger.getLogger(Model.class.getName()).log(Level.SEVERE, e.getMessage());
            throw new RuntimeException(e);
        }

        Category newCategory = new Category(newCategoryId, label, color);
        categories.add(newCategory);
    }

    /**
     * Remove a transaction from the list of transactions
     * @param transaction the transaction to remove
     */
    public void removeTransaction(Transaction transaction) {
        int removedTransactionId;
        try {
            removedTransactionId = databaseManager.removeTransaction(this.currentUser.id(), transaction.id());
        } catch (SQLException e) {
            Logger.getLogger(Model.class.getName()).log(Level.SEVERE, e.getMessage());
            throw new RuntimeException(e);
        }

        Logger.getLogger(Model.class.getName()).log(Level.FINE, "Removed transaction id: " + removedTransactionId);
        transactions.remove(transaction);
    }

    /**
     * Remove a category from the set of categories
     * @param category the category to remove
     */
    public void removeCategory(Category category) {
        if (this.transactions.stream().anyMatch(transaction -> transaction.category().equals(category))){
            throw new RuntimeException("Unable to remove category: " + category + " because it is used in at least one transaction");
        }

        int removedCategoryId;
        try {
            removedCategoryId = databaseManager.removeCategory(this.currentUser.id(), category.id());
        } catch (SQLException e) {
            Logger.getLogger(Model.class.getName()).log(Level.SEVERE, e.getMessage());
            throw new RuntimeException(e);
        }

        Logger.getLogger(Model.class.getName()).log(Level.FINE, "Removed category id: " + removedCategoryId);
        categories.remove(category);
    }

    /** Get a category by its label
     * @param categoryLabel the label of the category
     * @return the category with the given label
     */
    public Category getCategoryByLabel(String categoryLabel) {
        return categories.stream()
                .filter(category -> category.label().equals(categoryLabel))
                .findFirst()
                .orElse(null);
    }

    private String hashPassword(String plainTextPassword){
        return BCrypt.hashpw(plainTextPassword, BCrypt.gensalt());
    }

    private boolean passwordsMatch(String plainPassword, String hashedPassword) {
        return BCrypt.checkpw(plainPassword, hashedPassword);
    }

    /**
     * Get the current user
     * @return the current user
     */
    public String getUsername() {
        return this.currentUser.username();
    }

    /**
     * Get the current user's id
     * @return the current user's id
     */
    public String getUserEmail() {
        return this.currentUser.email();
    }
}