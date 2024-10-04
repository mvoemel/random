import { applyAttrs, removeElement, replaceElement } from "./utils";
import { render } from "./render";
import { NodeCache, Patch, PatchType } from "./types";

function applyPatch(patch: Patch, nodeCache: NodeCache): void {
  // Execute patch
  switch (patch.type) {
    case PatchType.PROPS:
      applyAttrs(patch.$Node as HTMLElement, patch.attributes);
      return;

    case PatchType.TEXT:
      patch.$Node.textContent = patch.value;
      return;

    case PatchType.REMOVE:
      removeElement(patch.$Node);
      return;

    case PatchType.REPLACE:
      const toReplace: Node = patch.$Node;
      const replacement: Node = render(patch.vNode, nodeCache);
      replaceElement(replacement, toReplace);
      return;

    case PatchType.APPEND:
      const parentNode = patch.$Node;
      const toAppend = render(patch.vNode, nodeCache);
      parentNode.appendChild(toAppend);
      return;
  }
}

function applyPatches(patches: Array<Patch>, nodeCache: NodeCache): void {
  // Loop through patches
  for (const patch of patches) {
    applyPatch(patch, nodeCache);
  }
}

export { applyPatches };
