import {
  VNode,
  VNodeAttributes,
  VElementNode,
  VTextNode,
  NodeCache,
  VNodeType,
  Patch,
  PatchType,
} from "./types";

function diff(
  oldNode: VNode,
  newNode: VNode,
  nodeCache: NodeCache
): Array<Patch> {
  const patches: Array<Patch> = [];
  runDiff(oldNode, newNode, patches, nodeCache);
  return patches;
}

function runDiff(
  oldNode: VNode,
  newNode: VNode,
  patches: Array<Patch>,
  nodeCache: NodeCache
): void {
  if (oldNode === newNode) {
    // Nodes are the same, assume no changes.
    return;
  } else {
    const $Node: Node = nodeCache.replace(oldNode, newNode);

    if (oldNode.type !== newNode.type) {
      // Different node types! Blow it up!
      patches.push({
        type: PatchType.REPLACE,
        vNode: newNode,
        $Node,
      });
    } else {
      // Same node type. More work to do.
      switch (oldNode.type) {
        case VNodeType.TEXT:
          if (oldNode.value !== (newNode as VTextNode).value) {
            patches.push({
              type: PatchType.TEXT,
              value: (newNode as VTextNode).value,
              $Node,
            });
          }
          return;

        case VNodeType.ELEMENT:
          if (oldNode.tagName !== (newNode as VElementNode).tagName) {
            patches.push({
              type: PatchType.REPLACE,
              vNode: newNode,
              $Node,
            });
          } else {
            const propsDiff: VNodeAttributes | undefined = diffAttrs(
              oldNode.attributes,
              (newNode as VElementNode).attributes
            );

            if (propsDiff !== undefined) {
              patches.push({
                type: PatchType.PROPS,
                attributes: propsDiff,
                $Node,
              });
            }

            diffChildren(
              oldNode,
              newNode as VElementNode,
              $Node as HTMLElement,
              patches,
              nodeCache
            );
          }
          return;

        default:
          const _exhaustiveCheck: never = oldNode;
          throw new Error(`Non-exhaustive match for ${_exhaustiveCheck}`);
      }
    }
  }
}

function diffChildren<T>(
  oldParent: VElementNode,
  newParent: VElementNode,
  parentNode: HTMLElement,
  patches: Array<Patch>,
  nodeCache: NodeCache
): void {
  const oldChildren: Array<VNode> = oldParent.children;
  const newChildren: Array<VNode> = newParent.children;
  const len: number = Math.max(oldChildren.length, newChildren.length);

  for (let i = 0; i < len; i++) {
    const oldChild = oldChildren[i];
    const newChild = newChildren[i];

    // APPEND NEW
    if (oldChild === undefined) {
      patches.push({
        type: PatchType.APPEND,
        vNode: newChild,
        $Node: parentNode,
      });

      // REMOVE OLD
    } else if (newChild === undefined) {
      patches.push({
        type: PatchType.REMOVE,
        $Node: nodeCache.get(oldChild)!,
      });

      // DIFF THE REST
    } else {
      runDiff(oldChild, newChild, patches, nodeCache);
    }
  }
}

function diffAttrs(
  oldAttrs: VNodeAttributes,
  newAttrs: VNodeAttributes
): VNodeAttributes | undefined {
  let _diff: VNodeAttributes | undefined;

  for (const key in oldAttrs) {
    if (oldAttrs[key] !== newAttrs[key]) {
      _diff = _diff || {};
      _diff[key] = newAttrs[key];
    }
  }

  for (const key in newAttrs) {
    if (oldAttrs[key] === undefined) {
      _diff = _diff || {};
      _diff[key] = newAttrs[key];
    }
  }

  return _diff;
}

export { diff };
