type AppState = {
  route: "/dashboard" | "/settings";
  username: string;
  settings: { email: string; position: string };
};

let appState: AppState = {
  route: "/dashboard",
  username: "John Doe",
  settings: { email: "john.doe@example.com", position: "Software Engineer" },
};

export { type AppState, appState };
