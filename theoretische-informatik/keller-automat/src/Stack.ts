interface StackInterface<T> {
  push(item: T): void;
  pop(): T | undefined;
  peek(): T | undefined;
  isEmpty(): boolean;
  size(): number;
  print(): void;
  get(): T[];
  toString(): string;
}

class Stack implements StackInterface<number> {
  private data: number[];

  constructor() {
    this.data = [];
  }

  push(item: number): void {
    this.data.push(item);
  }

  pop(): number | undefined {
    return this.data.pop();
  }

  peek(offset?: number): number | undefined {
    if (this.size() < 1 + (offset || 0)) return undefined;
    return this.data[this.size() - (1 + (offset || 0))];
  }

  isEmpty(): boolean {
    return this.size() === 0;
  }

  size(): number {
    return this.data.length;
  }

  print(): void {
    console.log(this.data.toString());
  }

  get(): number[] {
    return this.data;
  }

  toString(): string {
    return this.data.toString();
  }
}

export default Stack;
