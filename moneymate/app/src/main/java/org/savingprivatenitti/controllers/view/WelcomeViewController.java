package org.savingprivatenitti.controllers.view;

import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.stage.Stage;
import org.savingprivatenitti.ControllerFactory;

import java.io.IOException;


public class WelcomeViewController extends ViewController {

    @FXML
    private Button loginButton;

    @FXML
    private Button signUpButton;

    @FXML
    public void onLoginButtonClicked() throws IOException {
        setScene("/fxml/views/LoginView.fxml");
    }

    @FXML
    public void onSignUpButtonClicked() throws IOException {
        setScene("/fxml/views/SignUpView.fxml");
    }

    /**
     * Handle the event when the login button is clicked
     * @param stage the stage
     * @param controllerFactory the controller factory
     */
    public WelcomeViewController(Stage stage, ControllerFactory controllerFactory) {
        super(stage, controllerFactory);
    }

}
