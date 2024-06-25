package org.savingprivatenitti.controllers.view;

import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;
import org.savingprivatenitti.ControllerFactory;

import java.io.IOException;

abstract public class ViewController {

    protected Stage stage;
    protected ControllerFactory controllerFactory;

    /**
     * Create a new view controller
     * @param stage the stage
     * @param controllerFactory the controller factory
     */
    public ViewController(Stage stage, ControllerFactory controllerFactory) {
        this.stage = stage;
        this.controllerFactory = controllerFactory;
    }

    /**
     * Set the scene
     * @param fxmlPath the path to the fxml file
     * @throws IOException if the view cannot be loaded
     */
    protected void setScene(String fxmlPath) throws IOException {
        FXMLLoader fxmlLoader = new FXMLLoader(getClass().getResource(fxmlPath));
        fxmlLoader.setControllerFactory(controllerFactory);
        Parent root = fxmlLoader.load();
        Scene scene = stage.getScene();
        if (scene == null) {
            scene = new Scene(root);
        }
        scene.setRoot(root);
        stage.show();
    }

}
