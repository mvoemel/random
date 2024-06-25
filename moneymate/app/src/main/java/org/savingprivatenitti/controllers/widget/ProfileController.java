package org.savingprivatenitti.controllers.widget;

import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.text.Font;
import javafx.scene.text.Text;
import org.savingprivatenitti.models.Model;
import org.savingprivatenitti.utils.TextFormatter;

import java.net.URL;
import java.util.ResourceBundle;

public class ProfileController extends WidgetController implements Initializable {

    @FXML
    private Text usernameText;

    @FXML
    private Text emailText;

    /**
     * Create a new WidgetController
     *
     * @param model the model
     */
    public ProfileController(Model model) {
        super(model);
    }

    @Override
    public void initialize(URL location, ResourceBundle resources) {
        String usernameText = TextFormatter.shortenTextToFit(model.getUsername(), 50, new Font(14));
        String emailText = TextFormatter.shortenTextToFit(model.getUserEmail(), 80, new Font(14));
        setUsernameText(usernameText);
        setEmailText(emailText);
    }

    /**
     * Set the username text
     * @param username the username
     */
    public void setUsernameText(String username) {
        usernameText.setText(username);
    }

    /**
     * Set the email text
     * @param userEmail the email
     */
    public void setEmailText(String userEmail) {
        emailText.setText(userEmail);
    }

}
