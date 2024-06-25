package org.savingprivatenitti.models;

import javafx.scene.paint.Color;
import org.savingprivatenitti.TransactionType;

import java.sql.*;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 * DatabaseManager class provides methods to interact with a SQLite database.
 * It handles the creation and management of users, categories, and transactions.
 */
public class DatabaseManager {
    private static final String DATABASE_URL = "jdbc:sqlite:data.db";
    private static Connection connection;

    /**
     * Constructor for the DatabaseManager class.
     */
    public DatabaseManager() {
        try {
            connection = DriverManager.getConnection(DATABASE_URL);
            initDatabase();
            Logger.getLogger(DatabaseManager.class.getName()).log(Level.FINE, "Connected to database.");
        } catch (SQLException e) {
            Logger.getLogger(DatabaseManager.class.getName()).log(Level.SEVERE, "Error connecting to database: " + e.getMessage());
            throw new RuntimeException(e);
        }
    }

    /**
     * Initializes the database connection and creates the necessary tables.
     */
    private void initDatabase() {
        try (Statement stmt = connection.createStatement()) {
            // Create User Table if it doesn't already exist
            String createUsersTableSQM = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, email TEXT, password TEXT)";
            stmt.execute(createUsersTableSQM);

            // Create Category Table if it doesn't already exist
            String createCategoriesTableSQM = "CREATE TABLE IF NOT EXISTS categories (id INTEGER PRIMARY KEY, label TEXT, color TEXT, user_id INTEGER, FOREIGN KEY (user_id) REFERENCES users(id))";
            stmt.execute(createCategoriesTableSQM);

            // Create Transaction Table if it doesn't already exist
            String createTransactionsTableSQM = "CREATE TABLE IF NOT EXISTS transactions (id INTEGER PRIMARY KEY, type TEXT, amount REAL, date DATE, category_id INTEGER, user_id INTEGER, FOREIGN KEY (category_id) REFERENCES categories(id), FOREIGN KEY (user_id) REFERENCES users(id))";
            stmt.execute(createTransactionsTableSQM);

            Logger.getLogger(DatabaseManager.class.getName()).log(Level.FINE, "Database and tables created successfully (if needed).");
        } catch (SQLException e) {
            Logger.getLogger(DatabaseManager.class.getName()).log(Level.SEVERE, "Error initializing database: " + e.getMessage());
        }
    }

    /**
     * Retrieves all transactions for a given user ID.
     *
     * @param userId the ID of the user whose transactions to retrieve
     * @return a list of transactions for the specified user ID
     * @throws SQLException if there is an error connecting to the database or retrieving the transactions
     */
    public List<Transaction> getAllTransactions(int userId) throws SQLException {
        String sql = "SELECT * FROM transactions JOIN categories ON transactions.category_id = categories.id WHERE transactions.user_id = ?;";
        PreparedStatement preparedStatement;
        ResultSet resultSet;
        List<Transaction> transactions = new ArrayList<>();
        try {
            preparedStatement = connection.prepareStatement(sql);
            preparedStatement.setInt(1, userId);
            resultSet = preparedStatement.executeQuery();

            while (resultSet.next()) {
                int id = resultSet.getInt("id");
                String type = resultSet.getString("type");
                double amount = resultSet.getDouble("amount");
                Date date = resultSet.getDate("date");
                Category category = new Category(
                        resultSet.getInt("category_id"),
                        resultSet.getString("label"),
                        Color.web(resultSet.getString("color"))
                );
                transactions.add(new Transaction(id, Enum.valueOf(TransactionType.class, type), amount, date.toLocalDate(), category));
            }
        } catch (SQLException e) {
            Logger.getLogger(DatabaseManager.class.getName()).log(Level.SEVERE, "(getAllTransactions): Unable to get transactions: " + e.getMessage());
            throw new SQLException("(getAllTransactions): Unable to get transactions: " + e.getMessage());
        }

        return transactions;
    }

    /**
     * Retrieves all categories for a given user ID.
     *
     * @param userId the ID of the user whose categories to retrieve
     * @return a set of categories for the specified user ID
     * @throws SQLException if there is an error connecting to the database or retrieving the categories
     */
    public Set<Category> getAllCategories(int userId) throws SQLException {
        String sql = "SELECT * FROM categories WHERE user_id = ?;";
        PreparedStatement preparedStatement;
        ResultSet resultSet;
        Set<Category> categories = new HashSet<>();
        try {
            preparedStatement = connection.prepareStatement(sql);
            preparedStatement.setInt(1, userId);
            resultSet = preparedStatement.executeQuery();

            while (resultSet.next()) {
                categories.add(new Category(
                        resultSet.getInt("id"),
                        resultSet.getString("label"),
                        Color.web(resultSet.getString("color"))
                ));
            }
        } catch (SQLException e) {
            Logger.getLogger(DatabaseManager.class.getName()).log(Level.SEVERE, "(getAllCategories): Unable to get categories: " + e.getMessage());
            throw new SQLException("(getAllCategories): Unable to get categories: " + e.getMessage());
        }

        return categories;
    }

    /**
     * Adds a new transaction to the database.
     *
     * @param userId the ID of the user to associate with the transaction
     * @param type the type of the transaction
     * @param amount the amount of the transaction
     * @param date the date of the transaction
     * @param category the category associated with the transaction
     * @return the ID of the newly added transaction
     * @throws SQLException if there is an error connecting to the database or adding the transaction
     */
    public int addTransaction(int userId, TransactionType type, double amount, LocalDate date, Category category) throws SQLException {
        String sql = "INSERT INTO transactions (type, amount, date, category_id, user_id) VALUES (?,?,?,?,?)";
        PreparedStatement preparedStatement;

        try {
            preparedStatement = connection.prepareStatement(sql);
            preparedStatement.setString(1, type.toString());
            preparedStatement.setDouble(2, amount);
            preparedStatement.setDate(3, Date.valueOf(date));
            preparedStatement.setInt(4, category.id());
            preparedStatement.setInt(5, userId);
            preparedStatement.execute();
        } catch (SQLException e) {
            Logger.getLogger(DatabaseManager.class.getName()).log(Level.SEVERE, "(addTransaction): Unable to add transaction: " + e.getMessage());
            throw new SQLException("(addTransaction): Unable to add transaction: " + e.getMessage());
        }

        Statement statementTwo = connection.createStatement();
        ResultSet resultSetTwo;
        int last_insert_rowid;
        try {
            resultSetTwo = statementTwo.executeQuery("SELECT last_insert_rowid();");
            if (!resultSetTwo.next()) {
                throw new SQLException("(addTransaction): Unable to get last insert rowid.");
            }

            last_insert_rowid = resultSetTwo.getInt("last_insert_rowid()");
        } catch (SQLException e) {
            Logger.getLogger(DatabaseManager.class.getName()).log(Level.SEVERE, "(addTransaction): Unable to get last insert rowid.");
            throw new SQLException("(addTransaction): Unable to get last insert rowid.");
        }

        return last_insert_rowid;
    }

    /**
     * Adds a new category to the database.
     *
     * @param userId the ID of the user to associate with the category
     * @param label the label of the category
     * @param color the color of the category
     * @return the ID of the newly added category
     * @throws SQLException if there is an error connecting to the database or adding the category
     */
    public int addCategory(int userId, String label, Color color) throws SQLException {
        String sql = "INSERT INTO categories (label, color, user_id) VALUES (?,?,?)";
        PreparedStatement preparedStatement;

        try {
            preparedStatement = connection.prepareStatement(sql);
            preparedStatement.setString(1, label);
            preparedStatement.setString(2, color.toString());
            preparedStatement.setInt(3, userId);
            preparedStatement.execute();
        } catch (SQLException e) {
            Logger.getLogger(DatabaseManager.class.getName()).log(Level.SEVERE, "(addCategory): Unable to add category: " + e.getMessage());
            throw new SQLException("(addCategory): Unable to add category: " + e.getMessage());
        }

        Statement statementTwo = connection.createStatement();
        ResultSet resultSetTwo;
        int last_insert_rowid;
        try {
            resultSetTwo = statementTwo.executeQuery("SELECT last_insert_rowid();");
            if (!resultSetTwo.next()) {
                throw new SQLException("(addCategory): Unable to get last insert rowid.");
            }

            last_insert_rowid = resultSetTwo.getInt("last_insert_rowid()");
        } catch (SQLException e) {
            Logger.getLogger(DatabaseManager.class.getName()).log(Level.SEVERE, "(addCategory): Unable to get last insert rowid.");
            throw new SQLException("(addCategory): Unable to get last insert rowid.");
        }

        return last_insert_rowid;
    }

    /**
     * Removes a category from the database by its ID and associated user.
     *
     * @param userId the ID of the user whose category to remove
     * @param id the ID of the category to remove
     * @return the ID of the removed category
     * @throws SQLException if there is an error connecting to the database or removing the category
     */
    public int removeCategory(int userId, int id) throws SQLException {
        String sql = "DELETE FROM categories WHERE id = ? AND user_id = ?;";
        PreparedStatement preparedStatement;

        try {
            preparedStatement = connection.prepareStatement(sql);
            preparedStatement.setInt(1, id);
            preparedStatement.setInt(2, userId);
            preparedStatement.execute();
        } catch (SQLException e) {
            Logger.getLogger(DatabaseManager.class.getName()).log(Level.SEVERE, "(removeCategory): Unable to remove category: " + e.getMessage());
            throw new SQLException("(removeCategory): Unable to remove category: " + e.getMessage());
        }

        return id;
    }

    /**
     * Removes a transaction from the database by its ID and associated user.
     *
     * @param userId the ID of the user whose transaction to remove
     * @param id the ID of the transaction to remove
     * @return the ID of the removed transaction
     * @throws SQLException if there is an error connecting to the database or removing the transaction
     */
    public int removeTransaction(int userId, int id) throws SQLException {
        String sql = "DELETE FROM transactions WHERE id = ? AND user_id = ?;";
        PreparedStatement preparedStatement;

        try {
            preparedStatement = connection.prepareStatement(sql);
            preparedStatement.setInt(1, id);
            preparedStatement.setInt(2, userId);
            preparedStatement.execute();
        } catch (SQLException e) {
            Logger.getLogger(DatabaseManager.class.getName()).log(Level.SEVERE, "(removeTransaction): Unable to remove transaction: " + e.getMessage());
            throw new SQLException("(removeTransaction): Unable to remove transaction: " + e.getMessage());
        }

        return id;
    }

    /**
     * Retrieves a user by their ID from the database.
     *
     * @param userId the ID of the user to retrieve
     * @return the User object corresponding to the specified ID, or null if no user is found
     * @throws SQLException if there is an error connecting to the database or retrieving the user
     */
    public User getUserById(int userId) throws SQLException {
        String sql = "SELECT * FROM users WHERE id = ?;";
        PreparedStatement preparedStatement;
        ResultSet resultSet;
        User user;
        try {
            preparedStatement = connection.prepareStatement(sql);
            preparedStatement.setInt(1, userId);
            resultSet = preparedStatement.executeQuery();

            resultSet.next();

            user = new User(
                    resultSet.getInt("id"),
                    resultSet.getString("username"),
                    resultSet.getString("email"),
                    resultSet.getString("password")
            );
        } catch (SQLException e) {
            Logger.getLogger(DatabaseManager.class.getName()).log(Level.SEVERE, "(getUserById): Unable to get user: " + e.getMessage());
            throw new SQLException("(getUserById): Unable to get user: " + e.getMessage());
        }

        return user;
    }

    /**
     * Retrieves a user by their username from the database.
     *
     * @param username the username of the user to retrieve
     * @return the User object corresponding to the specified username, or null if no user is found
     * @throws SQLException if there is an error connecting to the database or retrieving the user
     */
    public User getUserByUsername(String username) throws SQLException {
        String sql = "SELECT * FROM users WHERE username = ?;";
        PreparedStatement preparedStatement;
        ResultSet resultSet;
        User user;
        try {
            preparedStatement = connection.prepareStatement(sql);
            preparedStatement.setString(1, username);
            resultSet = preparedStatement.executeQuery();

            resultSet.next();

            user = new User(
                    resultSet.getInt("id"),
                    resultSet.getString("username"),
                    resultSet.getString("email"),
                    resultSet.getString("password")
            );
        } catch (SQLException e) {
            Logger.getLogger(DatabaseManager.class.getName()).log(Level.SEVERE, "(getUserByUsername): Unable to get user: " + e.getMessage());
            throw new SQLException("(getUserByUsername): Unable to get user: " + e.getMessage());
        }

        return user;
    }

    /**
     * Adds a new user to the database.
     *
     * @param username the username of the new user
     * @param email the email of the new user
     * @param password the password of the new user
     * @return the ID of the newly added user
     * @throws SQLException if there is an error connecting to the database or adding the user
     */
    public int addNewUser(String username, String email, String password) throws SQLException {
        String sql = "INSERT INTO users (username, email, password) VALUES (?,?,?)";
        PreparedStatement preparedStatement;
        try {
            preparedStatement = connection.prepareStatement(sql);
            preparedStatement.setString(1, username);
            preparedStatement.setString(2, email);
            preparedStatement.setString(3, password);
            preparedStatement.execute();
        } catch (SQLException e) {
            Logger.getLogger(DatabaseManager.class.getName()).log(Level.SEVERE, "(addNewUser): Unable to add user: " + e.getMessage());
            throw new SQLException("(addNewUser): Unable to add user: " + e.getMessage());
        }

        Statement statementTwo = connection.createStatement();
        ResultSet resultSetTwo;
        int last_insert_rowid;
        try {
            resultSetTwo = statementTwo.executeQuery("SELECT last_insert_rowid();");
            if (!resultSetTwo.next()) {
                throw new SQLException("(addNewUser): Unable to get last insert rowid.");
            }

            last_insert_rowid = resultSetTwo.getInt("last_insert_rowid()");
        } catch (SQLException e) {
            Logger.getLogger(DatabaseManager.class.getName()).log(Level.SEVERE, "(addNewUser): Unable to get last insert rowid.");
            throw new SQLException("(addNewUser): Unable to get last insert rowid.");
        }

        return last_insert_rowid;
    }
}
