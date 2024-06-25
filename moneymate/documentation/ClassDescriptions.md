# Class descriptions

## `App`

This is the main class that contains the main method. It is responsible for starting the application.

## `Views`

### `SidebarOption`

This enum is used to define the different options that can be displayed in the sidebar.

### `ViewFactory`

This class is responsible for getting the correct view based on which view has been
selected by the user. It manages the creation of the different views.

## `Controllers`

### `MainController`

This controller is a key component of the application. It manages the different views
based on which option has been selected in the sidebar.

### `CategoryController`

This class is responsible for handling the logic for the category view. It 
contains methods for adding or deleting categories and manages the list
of available categories.

### `DashboardController` 

This controller is responsible for handling the logic for the dashboard view. It
manages the labels, charts and recent transactions displayed on the dashboard.

### `SidebarController`

This controller sets the sidebar option in the view factory based on which option
has been clicked in the sidebar. However, it **does not!** handle the logic for 
changing the view.

### `TransactionController`

This class contains a list of all transactions which is used in the views that needs transaction data.

### `WelcomeController`

This controller is responsible for handling the logic for the welcome view. It
contains a button that works as the start button.

### `TransactionCellController` 

This controller is responsible for handling the logic for the transaction cell view.
A transaction cell represents a single transaction in the transaction list.
Each cell has a delete button to delete the transaction.

## `Models`

### `Model` 

The model class holds the relationship between the views and 
controllers (MVC pattern). It holds the database and the viewfactory.

### `Database`

This class has access to the sqlite database and is responsible for handling all the database operations.
This includes adding transactions, categories, and deleting transactions, as well as getting all transactions and categories.

## `Utils`

### `DevModeUtil`

This is only used for enabling the development mode. This is useful
for testing and debugging the application.