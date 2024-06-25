# Class descriptions

## `App`

This is the main class that contains the main method. It is responsible for starting the application.

## `Models`

### `Model`

This class is responsible for storing and handling the data of the application. 
It contains observable lists for transactions and categories, aswell as methods to add transactions/categories
and delete transactions/categories. It also contains methods to get all transactions and categories.

The data is backed by our sqllite database.

### `Category` 

This class represents a category. It has a name, color and an id. 

### `Transaction` 

This class represents a transaction. It has a transaction type (income or expense),
an amount, a date, a category and an id.

### `User`

This class represents a user. It has a name, a username and a password. 

### `DatabaseManager`

This class is responsible for managing the database. It contains methods to create the database, 
create the tables, insert data, get data and delete data.

## `Controllers`

### `ViewControllers`

#### `ViewController`

This is the superclass of all view controllers. It contains 
the primary stage (the main stage of the application) and the controllerfactory.
It also contains a method to switch the view to another view using the fxmlPath as the parameter.


We decided to make this abstract class to avoid code duplication in the subclasses and to 
summarize the controllers that are responsible for switching the views. Since these controllers
don't show any data, they don't have access to the model and only get access to the properties 
they need. (Restricting access)

#### `WelcomeViewController`

This class is responsible for the welcome page. It handles the welcome button and redirects the user
to the login page.

#### `WelcomeViewController`

This class is responsible for the welcome page. It handles the welcome button and redirects the user
to the login page.

#### `AppViewController`

This class is responsible for switching the views between the different pages of the application.
The switching is handled by the buttons (menuitems) of the menubar, which calls the view switching methods
in the `AppViewController`. 

#### `LoginViewController`

This class is responsible for the login page. It handles the login button and also leads to the main page after
successful login. 

#### `LogoutController`

This class is responsible for the logout page. It handles the logout button and redirects the user
to the login page. 

#### `SignUpViewController`

This class is responsible for the sign up page. It handles the sign up button and 
creates a new user in the database. This user can then login with the credentials.

### `WidgetControllers`

#### `WidgetController`

This is the superclass of all widget controllers. Widget controllers are the controllers that display data.
Widgets are the small components that are displayed on the main page (the light dark boxes that a user can interact with).
It contains the model instance that is being used to get the data to display. 

We decided to make this abstract class to avoid code duplication in the subclasses. This also groups
all controllers that don't change the view but only display data, thus they don't need access to the stage
and views. They only need model access to display the data.

#### `AddNewCategoryWidgetController`

This class is responsible for the add new category widget. It handles the add button and adds a new category.

#### `AddNewEntryWidgetController`

This class is responsible for the add new entry widget. It handles the add button and adds a new transaction.
You can choose the category, the amount, the transaction type (income/expense) and the date of the transaction.

#### `BalanceStatsWidgetController` 

This class is responsible for the balance stats widget. It shows this week's income and expenses of the user.

#### `CategoriesChartWidgetController` 

This class is responsible for the categories chart widget. It shows the categories based on their expenses in a pie chart.
This is useful for the user to see where most of the money is spent.

#### `CategoriesListWidgetController`

This class is responsible for the categories list widget. It shows the categories created by the user. 

#### `RecentTransactionsWidgetController`

This class is responsible for the recent transactions widget. It shows the recent transactions of the user.

#### `TransactionsListWidgetController`

This class is responsible for the transactions list widget. It shows the entire transaction history of the user.

#### `WeeklySavingsOverviewWidgetController`

This class is responsible for the weekly savings overview widget. It shows the weekly savings of the user.
It's displayed as a stacked bar chart with red bars (for expense) and green bars (for income).
Since the expense will be substracted from the income, the user can see how much money he saved in a week (net income).

### `Primitive Controllers`

These are called "primitive", because they are the very basic/elemental
building blocks that are used in the application.

#### `CategoryController`

This controller handles the very basic "category box".
It automatically updates the color of the box based on the category color.

#### `TransactionController`

This controller handles the very basic "transaction box".
It automatically sets the color of the transaction category, handles the 
date and the amount of the transaction.

### `Modal`

#### `ModalController`

This is a controller for a modal dialog. It is static since we want to call it
in various places in the application. It is used for displaying a modal dialog.

### `ListItemController`

#### `CategoryListItemController`

This controller is responsible for the category list item. It handles the delete button and deletes the category.
This is used in combination of a scrollpane. 

#### `TransactionListItemController`

This controller is responsible for the transaction list item. It handles the delete button and deletes the transaction.
This is used in combination of a scrollpane.

## `Utils`

### `ColorConverter`

This class is used for converting to various color formats. 
It can convert JavaFX color objects to hex strings or rgb components for example.

### `DataFormatter`

This class is used for formatting data. It can format dates, numbers and currency.

### `TextFormatter`

This class is used for formatting text. It can format text to be displayed in the application.
It also contains a method that shortens texts that are too long.

### `DevModeUtil`

This is only used for enabling the development mode. This is useful
for testing and debugging the application.
