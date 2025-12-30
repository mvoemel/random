import { applyAttrs } from "./utils";
import {
  VNode,
  VNodeAttributes,
  VElementNode,
  VTextNode,
  NodeCache,
  VNodeType,
} from "./types";

function createText(node: VTextNode): Text {
  return document.createTextNode(node.value);
}

function createElement(node: VElementNode, nodeCache: NodeCache): HTMLElement {
  const element: HTMLElement = document.createElement(
    node.tagName
  ) as HTMLElement;
  const children: Array<VNode> = node.children;
  const len: number = children.length;

  applyAttrs(element, node.attributes);

  for (let i = 0; i < len; i++) {
    const childElement: Node = render(children[i], nodeCache);
    element.appendChild(childElement);
  }

  return element;
}

function render(node: VNode, nodeCache: NodeCache): Node {
  switch (node.type) {
    case VNodeType.ELEMENT:
      const element: HTMLElement = createElement(node, nodeCache);
      nodeCache.set(node, element);
      return element;

    case VNodeType.TEXT:
      const textNode: Text = createText(node);
      nodeCache.set(node, textNode);
      return textNode;

    default:
      const _exhaustiveCheck: never = node;
      throw new Error(`Non-exhaustive match for ${_exhaustiveCheck}`);
  }
}

export { render };
