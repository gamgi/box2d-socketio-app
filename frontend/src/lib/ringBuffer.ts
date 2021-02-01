export class RingBuffer {
  public buffer: number[];
  private pointer = 0;

  constructor(private size: number, initialValue: number) {
    if (size < 1) {
      throw new Error('Buffer size has to be at least 1');
    }
    this.buffer = new Array<number>(size).fill(initialValue);
  }

  public push(value: number): void {
    this.buffer[this.pointer] = value;
    this.pointer = (this.pointer + 1) % this.size;
  }

  public mean(): number {
    return this.buffer.reduce((acc, val) => acc + val, 0) / this.size;
  }
}
