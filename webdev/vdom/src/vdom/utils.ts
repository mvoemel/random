import { VNodeAttributes } from "./types";

function applyAttrs(element: HTMLElement, attrs: VNodeAttributes): void {
  for (const key in attrs) {
    if (attrs.hasOwnProperty(key)) {
      const value: string | undefined = attrs[key];

      if (value === undefined) {
        element.removeAttribute(key);
      } else {
        element.setAttribute(key, value);
      }
    }
  }
}

function removeElement(node: Node): void {
  const parentNode: Node | null = node.parentNode;

  if (parentNode !== null) {
    parentNode.removeChild(node);
  }
}

function replaceElement(replacement: Node, toReplace: Node): void {
  const parentNode: Node | null = toReplace.parentNode;

  if (parentNode !== null) {
    parentNode.replaceChild(replacement, toReplace);
  }
}

export { applyAttrs, removeElement, replaceElement };
