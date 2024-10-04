import { AppState } from "../state";
import { button, div } from "../vdom";

type NavbarProps = {
  appState: AppState;
};

function Navbar({ appState }: NavbarProps) {
  const dashboardActive = appState.route === "/dashboard" ? "green" : "white";
  const settingsActive = appState.route === "/settings" ? "green" : "white";

  return div(
    {
      style:
        "display: flex; justify-content: space-between; padding: 10px; background-color: #333; color: white;",
    },
    [
      div({ style: "display: flex;" }, [
        button(
          {
            id: "dashboard-button",
            style: `background-color: ${dashboardActive}; margin-right: 10px;`,
            // onclick: "handleRoute('/dashboard')",
          },
          ["Dashboard"]
        ),
        button(
          {
            id: "settings-button",
            style: `background-color: ${settingsActive};`,
            // onclick: "handleRoute('/settings')",
          },
          ["Settings"]
        ),
      ]),
      div({}, [`Logged in as: ${appState.username}`]),
    ]
  );
}

export default Navbar;
