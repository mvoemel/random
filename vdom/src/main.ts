import Dashboard from "./components/dashboard";
import Navbar from "./components/navbar";
import Settings from "./components/settings";
import { appState, AppState } from "./state";
import { div } from "./vdom/elements";
import { scene } from "./vdom/scene";

const getView = (route: AppState["route"]) => {
  return div({ class: "container" }, [
    Navbar({ appState }),
    route === "/dashboard" ? Dashboard() : Settings({ appState }),
  ]);
};

const schedule = scene(
  getView(appState.route),
  document.getElementById("root")
);

function handleRouteChange(route: AppState["route"]) {
  appState.route = route;
  schedule(getView(appState.route));
}

document
  .getElementById("dashboard-button")
  ?.addEventListener("click", () => handleRouteChange("/dashboard"));
document
  .getElementById("settings-button")
  ?.addEventListener("click", () => handleRouteChange("/settings"));
