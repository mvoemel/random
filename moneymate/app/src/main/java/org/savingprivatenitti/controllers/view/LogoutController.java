package org.savingprivatenitti.controllers.view;

import javafx.fxml.FXML;
import javafx.scene.image.ImageView;
import javafx.scene.text.Text;
import javafx.stage.Stage;
import org.savingprivatenitti.ControllerFactory;

import java.io.IOException;
import java.util.function.Supplier;
import java.util.logging.Level;
import java.util.logging.Logger;

public class LogoutController extends ViewController {

    @FXML
    private ImageView logoutButton;

    @FXML
    private Text username;

    @FXML
    private Text email;

    private Supplier<Boolean> setOnLogout;

    @FXML
    public void onLogoutSymbolClicked() throws IOException {
        boolean logoutResult = false;
        if (setOnLogout != null) {
            logoutResult = setOnLogout.get();
        }
        if (logoutResult) {
            setScene("/fxml/views/LoginView.fxml");
        } else {
            Logger.getLogger(LogoutController.class.getName()).log(Level.WARNING, "Failed to log out");
        }
    }

    /**
     * Create a new view controller
     *
     * @param stage             the stage
     * @param controllerFactory the controller factory
     */
    public LogoutController(Stage stage, ControllerFactory controllerFactory) {
        super(stage, controllerFactory);
    }

    /**
     * Set the onLogout function
     * @param setOnLogout the onLogout function
     */
    public void setOnLogout(Supplier<Boolean> setOnLogout) {
        this.setOnLogout = setOnLogout;
    }

    /**
     * Set the username text
     * @param username the username
     */
    public void setUsernameText(String username) {
        this.username.setText(username);
    }

    /**
     * Set the email text
     * @param email the email
     */
    public void setEmailText(String email) {
        this.email.setText(email);
    }
}
