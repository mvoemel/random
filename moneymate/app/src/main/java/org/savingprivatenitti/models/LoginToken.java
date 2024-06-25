package org.savingprivatenitti.models;

/**
 * A record representing a login token
 * @param username the username
 * @param password the password
 */
public record LoginToken(String username, String password) {
}
