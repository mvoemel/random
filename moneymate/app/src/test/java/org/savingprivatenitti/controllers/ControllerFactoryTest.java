package org.savingprivatenitti.controllers;

import javafx.stage.Stage;
import org.junit.jupiter.api.Test;
import org.savingprivatenitti.*;
import org.savingprivatenitti.models.Model;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.mock;

//Test that a newly created ControllerFactory object won't be null
public class ControllerFactoryTest {

    @Test
    public void testConstructor() {
        Stage stage = mock(Stage.class);
        Model model = mock(Model.class);
        ControllerFactory controllerFactory = new ControllerFactory(stage, model);
        assertNotNull(controllerFactory);
    }
}
