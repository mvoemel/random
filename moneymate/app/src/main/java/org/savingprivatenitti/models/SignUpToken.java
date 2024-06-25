package org.savingprivatenitti.models;

/**
 * A record representing a sign up token
 * @param username the username
 * @param email the email
 * @param password the password
 */
public record SignUpToken(String username, String email, String password) {
}
