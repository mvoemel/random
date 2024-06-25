package org.savingprivatenitti.controllers.widget;

import javafx.animation.ScaleTransition;
import javafx.scene.Node;
import javafx.util.Duration;
import org.savingprivatenitti.models.Model;

public abstract class WidgetController {

    protected Model model;
    protected Node scalableNode;

    /**
     * Create a new WidgetController
     * @param model the model
     */
    public WidgetController(Model model) {
        this.model = model;
    }

    /**
     * Apply a scale effect to the scalableNode
     */
    protected void applyScaleEffect() {
        ScaleTransition stGrow = new ScaleTransition(Duration.millis(200), scalableNode);
        stGrow.setFromX(1);
        stGrow.setFromY(1);
        stGrow.setToX(1.02);
        stGrow.setToY(1.02);

        ScaleTransition stShrink = new ScaleTransition(Duration.millis(200), scalableNode);
        stShrink.setFromX(1.02);
        stShrink.setFromY(1.02);
        stShrink.setToX(1);
        stShrink.setToY(1);

        // Apply the ScaleTransition when the mouse enters the scalableNode
        scalableNode.setOnMouseEntered(e -> {
            stShrink.stop();
            stGrow.playFromStart();
        });

        // Apply the shrink transition when the mouse exits the scalableNode
        scalableNode.setOnMouseExited(e -> {
            stGrow.stop();
            stShrink.playFromStart();
        });
    }

}