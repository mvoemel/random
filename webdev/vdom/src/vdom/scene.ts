import { diff } from "./diff";
import { applyPatches } from "./patches";
import { render } from "./render";
import { VNode, NodeCache } from "./types";

type Scheduler = (newView: VNode) => void;

function scene(initialView: VNode, rootNode: HTMLElement | null): Scheduler {
  if (!rootNode) throw new Error("Root node not provided.");

  let savedView: VNode = initialView;

  const nodeCache: NodeCache = new NodeCache();
  const domNode: Node = render(initialView, nodeCache);

  rootNode.appendChild(domNode);

  return (newView: VNode): void => {
    const patches = diff(savedView, newView, nodeCache);
    applyPatches(patches, nodeCache);
    savedView = newView;
  };
}

export { type Scheduler, scene };
