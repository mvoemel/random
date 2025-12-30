import { div, h2, table, td, th, tr } from "../vdom";

function Dashboard() {
  return div({ style: "padding: 20px;" }, [
    h2({}, ["Dashboard"]),
    table({ border: "1", width: "100%" }, [
      tr({}, [th({}, ["Name"]), th({}, ["Age"])]),
      tr({}, [td({}, ["Alice"]), td({}, ["30"])]),
      tr({}, [td({}, ["Bob"]), td({}, ["25"])]),
    ]),
  ]);
}

export default Dashboard;
