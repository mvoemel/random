package org.savingprivatenitti.controllers.view;

import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.scene.control.Hyperlink;
import javafx.scene.control.TextField;
import javafx.stage.Stage;
import org.savingprivatenitti.ControllerFactory;
import org.savingprivatenitti.models.SignUpToken;
import org.savingprivatenitti.controllers.modal.Modal;

import java.io.IOException;
import java.util.function.Function;

public class SignUpViewController extends ViewController {

    @FXML
    private TextField email;

    @FXML
    private TextField username;

    @FXML
    private TextField password;

    @FXML
    private Hyperlink loginLink;

    @FXML
    private Button signUpButton;

    private Function<SignUpToken, Boolean> onSignUp;

    @FXML
    public void onLoginLinkClicked() throws Exception {
        setScene("/fxml/views/LoginView.fxml");
    }

    @FXML
    public void onSignUpButtonClicked() throws IOException {
        boolean signUpResult = false;
        if (onSignUp != null) {
            signUpResult = onSignUp.apply(new SignUpToken(username.getText(), email.getText(), password.getText()));
        }
        if (signUpResult) {
            setScene("/fxml/views/DashboardView.fxml");
        } else {
            Modal.showMessage("Sign up failed!");
        }
        setScene("/fxml/views/LoginView.fxml");
    }

    /**
     * Handle the event when the login link is clicked
     * @param stage the stage
     * @param controllerFactory the controller factory
     */
    public SignUpViewController(Stage stage, ControllerFactory controllerFactory) {
        super(stage, controllerFactory);
    }

    /**
     * Set the onSignUp function
     * @param onSignUp the onSignUp function
     */
    public void setSignUpFunction(Function<SignUpToken, Boolean> onSignUp) {
        this.onSignUp = onSignUp;
    }
}
