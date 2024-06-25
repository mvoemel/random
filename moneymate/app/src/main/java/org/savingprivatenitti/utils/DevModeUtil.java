package org.savingprivatenitti.utils;

public class DevModeUtil {
    private static final boolean DEV_MODE = Boolean.parseBoolean(System.getProperty("devMode"));

    /**
     * Check if the application is in development mode
     * @return true if the application is in development mode, false otherwise
     */
    public static boolean isDevMode() {
        return DEV_MODE;
    }
}
