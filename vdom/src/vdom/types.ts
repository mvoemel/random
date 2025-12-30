enum VNodeType {
  ELEMENT,
  TEXT,
}

type VNodeAttributes = {
  [name: string]: string | undefined;
};

type VElementNode = {
  type: VNodeType.ELEMENT;
  tagName: string; // TODO: specify valid HTML tags
  attributes: VNodeAttributes;
  children: Array<VNode>;
};

type VTextNode = {
  type: VNodeType.TEXT;
  value: string;
};

type VNode = VElementNode | VTextNode;

// TODO: remove this line ------------------------------------

enum PatchType {
  APPEND,
  REPLACE,
  REMOVE,
  PROPS,
  TEXT,
}

type AppendPatch = {
  type: PatchType.APPEND;
  vNode: VNode;
  $Node: Node;
};

type ReplacePatch = {
  type: PatchType.REPLACE;
  vNode: VNode;
  $Node: Node;
};

type RemovePatch = {
  type: PatchType.REMOVE;
  $Node: Node;
};

type PropsPatch = {
  type: PatchType.PROPS;
  attributes: VNodeAttributes;
  $Node: Node;
};

type TextPatch = {
  type: PatchType.TEXT;
  value: string;
  $Node: Node;
};

type Patch = AppendPatch | ReplacePatch | RemovePatch | PropsPatch | TextPatch;

class NodeCache extends WeakMap<VNode, Node> {
  public replace(oldKey: VNode, newKey: VNode): Node {
    // If the node is not in cache something is very wrong.
    const value: Node = this.get(oldKey)!;
    this.delete(oldKey);
    this.set(newKey, value);
    return value;
  }
}

export {
  VNodeType,
  VNodeAttributes,
  VElementNode,
  VTextNode,
  VNode,
  PatchType,
  AppendPatch,
  ReplacePatch,
  RemovePatch,
  PropsPatch,
  TextPatch,
  Patch,
  NodeCache,
};
