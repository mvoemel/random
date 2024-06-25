/*
 * This file was generated by the Gradle 'init' task.
 *
 * This generated file contains a sample Java application project to get you started.
 * For more details on building Java & JVM projects, please refer to https://docs.gradle.org/8.7/userguide/building_java_projects.html in the Gradle documentation.
 */

plugins {
    // Apply the application plugin to add support for building a CLI application in Java.
    application
    id("org.openjfx.javafxplugin") version "0.1.0"
}

repositories {
    // Use Maven Central for resolving dependencies.
    mavenCentral()
}

dependencies {
    // Use JUnit Jupiter for testing.
    testImplementation(libs.junit.jupiter)
    testImplementation("org.powermock:powermock-api-mockito2:2.0.9")
    testImplementation("org.powermock:powermock-module-junit4:2.0.9")
    testRuntimeOnly("org.junit.platform:junit-platform-launcher")

    // This dependency is used by the application.
    implementation(libs.guava)

    // SQLite3 Database Driver
    implementation("org.xerial:sqlite-jdbc:3.44.1.0")

    // Font Awesome JavaFX Icon Library
    implementation("de.jensd:fontawesomefx-fontawesome:4.7.0-9.1.2")

    implementation("org.mockito:mockito-core:5.11.0")

    // BCrypt Password Hashing Library
    implementation("org.mindrot:jbcrypt:0.4")
}

// Apply a specific Java toolchain to ease working on different environments.
java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
    }
}

application {
    // Define the main class for the application.
    mainClass = "org.savingprivatenitti.App"
}

javafx {
    version = "21.0.2"
    modules("javafx.controls", "javafx.fxml")
}

tasks.named<Test>("test") {
    // Use JUnit Platform for unit tests.
    useJUnitPlatform()
}

tasks.register<JavaExec>("dev") {
    mainClass.set("org.savingprivatenitti.App")
    classpath = sourceSets["main"].runtimeClasspath
    systemProperty("devMode", project.findProperty("devMode") ?: "false")

    jvmArgs = listOf(
        "--module-path", classpath.asPath,
        "--add-modules", "javafx.controls,javafx.fxml"
    )
}