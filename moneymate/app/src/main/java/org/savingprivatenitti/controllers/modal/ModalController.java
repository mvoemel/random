package org.savingprivatenitti.controllers.modal;

import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.scene.text.Text;
import javafx.stage.Stage;

import java.util.logging.Level;
import java.util.logging.Logger;

public class ModalController {
    @FXML
    private Text modalText;

    @FXML
    private Button okButton;

    /**
     * Handle the event when the ok button is clicked
     */
    @FXML
    public void onOkButtonClicked() {
        Stage stage = (Stage) okButton.getScene().getWindow();
        stage.close();
        Logger.getLogger(ModalController.class.getName()).log(Level.INFO, "Modal closed");
    }

    /**
     * Set the message of the modal
     * @param message the message to set
     */
    public void setMessage(String message) {
        modalText.setText(message);
    }
}
