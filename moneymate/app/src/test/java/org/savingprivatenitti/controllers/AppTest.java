package org.savingprivatenitti.controllers;

import javafx.application.Application;
import javafx.application.Platform;
import javafx.stage.Stage;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.savingprivatenitti.App;

import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;

class AppTest {

    @BeforeAll
    public static void setup() throws InterruptedException {
        // Initialize JavaFX runtime
        Thread t = new Thread("JavaFX Init Thread") {
            public void run() {
                    Application.launch(App.class);
            }
        };
        t.setDaemon(true);
        t.start();
        Thread.sleep(500);  // Add a delay to give JavaFX time to initialize
    }

    @AfterAll
    public static void tearDown() {
        Platform.runLater(Platform::exit);
    }

    @Test
    public void testStart() throws Exception {
        Stage stage = Mockito.mock(Stage.class);
        App app = Mockito.mock(App.class);

        Platform.runLater(() -> {
            try {
                app.start(stage);
            } catch (Exception e) {
                e.printStackTrace();
            }
        });

        // Add a delay to wait for the UI operation to complete
        Thread.sleep(1000);

        verify(app, times(1)).start(stage);
    }
}
