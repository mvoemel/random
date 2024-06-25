package org.savingprivatenitti;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.image.Image;
import javafx.scene.text.Font;
import javafx.stage.Stage;
import org.savingprivatenitti.models.Model;
import org.savingprivatenitti.utils.DevModeUtil;

import java.io.IOException;
import java.util.Objects;
import java.util.logging.Level;
import java.util.logging.Logger;

public class App extends Application {

    private final Model model = new Model();

    /**
     * Start method for the application
     * @param stage the primary stage for this application, onto which
     * the application scene can be set.
     * Applications may create other stages, if needed, but they will not be
     * primary stages.
     * @throws IOException if the FXML file is not found
     */
    @Override
    public void start(Stage stage) throws IOException {
        FXMLLoader fxmlLoader = new FXMLLoader(getClass().getResource("/fxml/views/WelcomeView.fxml"));
        ControllerFactory controllerFactory = new ControllerFactory(stage, model);
        fxmlLoader.setControllerFactory(controllerFactory);
        Parent root = fxmlLoader.load();
        Scene scene = new Scene(root);
        scene.getStylesheets().add(Objects.requireNonNull(getClass().getResource("/stylesheets/globals.css")).toExternalForm());
        stage.setTitle("Money Mate");
        Image logo = new Image(Objects.requireNonNull(getClass().getResourceAsStream("/images/logo.png")));
        stage.getIcons().add(logo);
        stage.setResizable(false);
        stage.setScene(scene);
        stage.show();
    }

    /**
     * Main method to launch the application
     * @param args command line arguments
     */
    public static void main(String[] args) {
        if (DevModeUtil.isDevMode()) Logger.getLogger(App.class.getName()).log(Level.CONFIG, "Application is running in development mode");
        System.setProperty("apple.awt.application.name", "Money Mate");
        System.setProperty("apple.awt.application.icon", "/images/logo.png");
        launch(args);
    }
}
