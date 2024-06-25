package org.savingprivatenitti;

import javafx.stage.Stage;
import javafx.util.Callback;
import org.savingprivatenitti.controllers.view.*;
import org.savingprivatenitti.controllers.widget.*;
import org.savingprivatenitti.models.Model;

import java.util.HashMap;
import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;

public class ControllerFactory implements Callback<Class<?>, Object> {

    private final Map<String, ViewController> viewControllerMap = new HashMap<>();
    private final Map<String, WidgetController> widgetControllerMap = new HashMap<>();
    private final Model model;

    /**
     * Constructor for the ControllerFactory
     * @param stage the primary stage for this application
     * @param model the model for this application
     */
    public ControllerFactory(Stage stage, Model model) {
        initializeViewControllerMap(stage);
        initializeWidgetControllerMap(model);
        this.model = model;
        setLoginViewFunction();
        setSignUpViewFunction();
        setLogoutViewFunction();
    }

    /**
     * Method to call the controller
     * @param type the class type of the controller
     * @return the controller object
     */
    @Override
    public Object call(Class<?> type) {
        if (WidgetController.class.isAssignableFrom(type)) {
            WidgetController widgetController = widgetControllerMap.get(type.getSimpleName());
            if (widgetController != null) {
                return widgetController;
            } else {
                Logger.getLogger(ControllerFactory.class.getName()).log(Level.WARNING, "Couldn't locate widget controller: " + type.getSimpleName());
                return null;
            }
        }
        ViewController viewController = viewControllerMap.get(type.getSimpleName());
        if (viewController != null) {
            return viewController;
        } else {
            Logger.getLogger(ControllerFactory.class.getName()).log(Level.WARNING, "Couldn't locate controller: " + type.getSimpleName());
            return null;
        }
    }

    private void setLoginViewFunction() {
        LoginViewController loginViewController = (LoginViewController) viewControllerMap.get("LoginViewController");
        loginViewController.setLoginFunction(model::login);
    }

    private void setSignUpViewFunction() {
        SignUpViewController signUpViewController = (SignUpViewController) viewControllerMap.get("SignUpViewController");
        signUpViewController.setSignUpFunction(model::signUp);
    }

    private void setLogoutViewFunction() {
        LogoutController logoutController = (LogoutController) viewControllerMap.get("LogoutController");
        logoutController.setOnLogout(model::logout);
    }

    private void initializeViewControllerMap(Stage stage) {
        // Instantiate all controllers and add them to the controller map
        ViewController welcomeViewController = new WelcomeViewController(stage, this);
        ViewController loginViewController = new LoginViewController(stage, this);
        ViewController signUpViewController = new SignUpViewController(stage, this);
        ViewController appViewController = new AppViewController(stage, this);
        ViewController logoutController = new LogoutController(stage, this);
        viewControllerMap.put("WelcomeViewController", welcomeViewController);
        viewControllerMap.put("LoginViewController", loginViewController);
        viewControllerMap.put("SignUpViewController", signUpViewController);
        viewControllerMap.put("AppViewController", appViewController);
        viewControllerMap.put("LogoutController", logoutController);
    }

    private void initializeWidgetControllerMap(Model model) {
        // Instantiate all widget controllers and add them to the widget controller map
        WidgetController recentTransactionsWidgetController = new RecentTransactionsWidgetController(model);
        WidgetController transactionsListWidgetController = new TransactionsListWidgetController(model);
        WidgetController addNewCategoryWidgetController = new AddNewCategoryWidgetController(model);
        WidgetController categoriesListWidgetController = new CategoriesListWidgetController(model);
        WidgetController balanceStatsWidgetController = new BalanceStatsWidgetController(model);
        WidgetController addNewEntryWidgetController = new AddNewEntryWidgetController(model);
        WidgetController weeklySavingsOverviewWidgetController = new WeeklySavingsOverviewWidgetController(model);
        WidgetController categoriesChartWidgetController = new CategoriesChartWidgetController(model);
        WidgetController profileController = new ProfileController(model);
        widgetControllerMap.put("RecentTransactionsWidgetController", recentTransactionsWidgetController);
        widgetControllerMap.put("TransactionsListWidgetController", transactionsListWidgetController);
        widgetControllerMap.put("AddNewCategoryWidgetController", addNewCategoryWidgetController);
        widgetControllerMap.put("CategoriesListWidgetController", categoriesListWidgetController);
        widgetControllerMap.put("BalanceStatsWidgetController", balanceStatsWidgetController);
        widgetControllerMap.put("AddNewEntryWidgetController", addNewEntryWidgetController);
        widgetControllerMap.put("WeeklySavingsOverviewWidgetController", weeklySavingsOverviewWidgetController);
        widgetControllerMap.put("CategoriesChartWidgetController", categoriesChartWidgetController);
        widgetControllerMap.put("ProfileController", profileController);
    }
}
