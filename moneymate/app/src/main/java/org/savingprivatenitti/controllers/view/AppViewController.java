package org.savingprivatenitti.controllers.view;

import javafx.animation.FadeTransition;
import javafx.animation.ParallelTransition;
import javafx.animation.TranslateTransition;
import javafx.application.Platform;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.Button;
import javafx.scene.layout.Pane;
import javafx.stage.Stage;
import javafx.util.Duration;
import org.savingprivatenitti.ControllerFactory;

import java.io.IOException;
import java.net.URL;
import java.util.ResourceBundle;

public class AppViewController extends ViewController implements Initializable {

    @FXML
    private Pane menubarActiveIndicator;

    @FXML
    private Button dashBoardMenuItem;

    @FXML
    private Button transactionsMenuItem;

    @FXML
    private Button categoriesMenuItem;

    /**
     * Switch to the dashboard view
     * @throws IOException if the view cannot be loaded
     */
    @FXML
    public void switchToDashboard() throws IOException {
        setScene("/fxml/views/DashboardView.fxml");
    }

    /**
     * Switch to the transaction view
     * @throws IOException if the view cannot be loaded
     */
    @FXML
    public void switchToTransaction() throws IOException {
        setScene("/fxml/views/TransactionsView.fxml");
    }

    /**
     * Switch to the category view
     * @throws IOException if the view cannot be loaded
     */
    @FXML
    public void switchToCategory() throws IOException {
        setScene("/fxml/views/CategoriesView.fxml");
    }

    /**
     * Constructor for the AppViewController
     * @param stage the primary stage for this application
     * @param controllerFactory the controller factory for this application
     */
    public AppViewController(Stage stage, ControllerFactory controllerFactory) {
        super(stage, controllerFactory);
    }

    @Override
    public void initialize(URL location, ResourceBundle resources) {
        applyEffectOnMenubarActiveIndicator();
    }

    /**
     * Apply effect on the menubar active indicator
     */
    public void applyEffectOnMenubarActiveIndicator() {
        Platform.runLater(() -> {
            TranslateTransition translateTransition = new TranslateTransition(Duration.millis(150), menubarActiveIndicator);
            translateTransition.setToX(10);

            FadeTransition fadeTransition = new FadeTransition(Duration.millis(150), menubarActiveIndicator);
            fadeTransition.setFromValue(0.0);
            fadeTransition.setToValue(1.0);

            ParallelTransition parallelTransition = new ParallelTransition(translateTransition, fadeTransition);
            parallelTransition.play();
        });
    }

}
