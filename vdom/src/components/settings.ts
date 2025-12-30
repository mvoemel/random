import { AppState } from "../state";
import { button, createVElementNode, div, h2 } from "../vdom";

type SettingsProps = {
  appState: AppState;
};

function Settings({ appState }: SettingsProps) {
  return div({ class: "nice-flex", style: "padding: 20px; width: 500px;" }, [
    h2({}, ["Settings"]),
    createVElementNode("label")({}, ["Email:"]),
    createVElementNode("input")(
      {
        style: "width: 100%",
        id: "email-input-field",
        type: "email",
        name: "email",
        value: appState.settings.email,
      },
      []
    ),
    createVElementNode("br")({}, []),
    createVElementNode("label")({}, ["Position:"]),
    createVElementNode("input")(
      {
        style: "width: 100%",
        id: "position-input-field",
        type: "text",
        name: "position",
        value: appState.settings.position,
      },
      []
    ),
    createVElementNode("br")({}, []),
    button(
      {
        onclick: "alert('Settings saved!')",
      },
      ["Save Settings"]
    ),
  ]);
}

export default Settings;
