import {
  VNode,
  VNodeAttributes,
  VElementNode,
  VTextNode,
  VNodeType,
} from "./types";

const vTextNode = (val: string): VTextNode => ({
  type: VNodeType.TEXT,
  value: val,
});

const vElementNode = (
  tagName: string,
  attributes: VNodeAttributes = {},
  children: Array<VNode | string> = []
): VElementNode => ({
  type: VNodeType.ELEMENT,
  tagName,
  attributes,
  children: children.map((next: VNode | string): VNode => {
    if (typeof next === "string") {
      return vTextNode(next);
    } else {
      return next;
    }
  }),
});

const createVElementNode =
  (tagName: string) =>
  (
    attributes: VNodeAttributes = {},
    children: Array<VNode | string>
  ): VElementNode =>
    vElementNode(tagName, attributes, children);

const div = createVElementNode("div");
const article = createVElementNode("article");
const section = createVElementNode("section");

const h1 = createVElementNode("h1");
const h2 = createVElementNode("h2");
const h3 = createVElementNode("h3");
const h4 = createVElementNode("h4");
const h5 = createVElementNode("h5");
const h6 = createVElementNode("h6");

const ul = createVElementNode("ul");
const ol = createVElementNode("ol");
const li = createVElementNode("li");

const table = createVElementNode("table");
const tr = createVElementNode("tr");
const td = createVElementNode("td");
const th = createVElementNode("th");

const button = createVElementNode("button");

export { vTextNode, vElementNode, createVElementNode };
export {
  div,
  article,
  section,
  h1,
  h2,
  h3,
  h4,
  h5,
  h6,
  ul,
  ol,
  li,
  table,
  tr,
  td,
  th,
  button,
};
