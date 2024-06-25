interface Delay {
  (time: number): Promise<void>;
}

export const delay: Delay = (time: number) => {
  return new Promise<void>((resolve) => setTimeout(resolve, time));
};
