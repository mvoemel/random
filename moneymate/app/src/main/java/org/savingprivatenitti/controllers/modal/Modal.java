package org.savingprivatenitti.controllers.modal;

import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Modality;
import javafx.stage.Stage;

import java.util.logging.Level;
import java.util.logging.Logger;

public class Modal {

    /**
     * Show a modal with a message
     * @param message the message to show
     */
    public static void showMessage(String message) {
        try {
            Stage modalStage = new Stage();
            FXMLLoader loader = new FXMLLoader(Modal.class.getResource("/fxml/modals/Modal.fxml"));
            Parent modalRoot = loader.load();

            // Assuming your modal's controller has a method setMessage
            ModalController modalController = loader.getController();
            modalController.setMessage(message);

            Scene modalScene = new Scene(modalRoot);
            modalScene.getStylesheets().add("/stylesheets/globals.css");
            modalStage.setScene(modalScene);
            modalStage.setResizable(false);
            modalStage.setAlwaysOnTop(true);

            modalStage.initModality(Modality.APPLICATION_MODAL);
            modalStage.showAndWait();
        } catch (Exception e) {
            Logger.getLogger(Modal.class.getName()).log(Level.SEVERE, "Error showing modal", e);
        }
    }
}
