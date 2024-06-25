package org.savingprivatenitti.controllers.view;

import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.scene.control.Hyperlink;
import javafx.scene.control.TextField;
import javafx.stage.Stage;
import org.savingprivatenitti.ControllerFactory;
import org.savingprivatenitti.models.LoginToken;
import org.savingprivatenitti.controllers.modal.Modal;

import java.io.IOException;
import java.util.function.Function;

public class LoginViewController extends ViewController {

    @FXML
    private TextField username;

    @FXML
    private TextField password;

    @FXML
    private Hyperlink signUpLink;

    @FXML
    private Button loginButton;

    private Function<LoginToken, Boolean> onLogin;

    /**
     * Handle the event when the sign up link is clicked
     * @throws Exception if the view cannot be loaded
     */
    @FXML
    public void onSignUpLinkClicked() throws Exception {
        setScene("/fxml/views/SignUpView.fxml");
    }

    /**
     * Handle the event when the login button is clicked
     * @throws IOException if the view cannot be loaded
     */
    @FXML
    public void onLoginButtonClicked() throws IOException {
        boolean loginResult = false;
        if (onLogin != null) {
            loginResult = onLogin.apply(new LoginToken(username.getText(), password.getText()));
        }
        if (loginResult) {
            setScene("/fxml/views/DashboardView.fxml");
        } else {
            Modal.showMessage("Wrong username or password!");
        }
    }

    /**
     * Handle the event when the login button is clicked
     * @param stage the stage
     * @param controllerFactory the controller factory
     */
    public LoginViewController(Stage stage, ControllerFactory controllerFactory) {
        super(stage, controllerFactory);
    }

    /**
     * Set the login function
     * @param onLogin the login function
     */
    public void setLoginFunction(Function<LoginToken, Boolean> onLogin) {
        this.onLogin = onLogin;
    }

}
