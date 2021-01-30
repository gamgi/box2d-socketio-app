import { RingBuffer } from './ringBuffer';
describe('RingBuffer', () => {
  it('initializes corect length', () => {
    const b = new RingBuffer(5, 0);
    expect(b.buffer).toEqual([0, 0, 0, 0, 0]);
  });

  it('push adds items to buffer', () => {
    const b = new RingBuffer(5, 0);
    b.push(1);
    b.push(2);
    expect(b.buffer).toEqual([1, 2, 0, 0, 0]);
  });

  it('mean returns buffer mean', () => {
    const b = new RingBuffer(5, 1);
    b.push(1);
    b.push(2);
    expect(b.mean()).toEqual(1.2);
  });

  it('loops to beginning when full', () => {
    const b = new RingBuffer(5, 1);
    b.push(1);
    b.push(2);
    b.push(3);
    b.push(4);
    b.push(5);
    b.push(6);
    expect(b.buffer).toEqual([6, 2, 3, 4, 5]);
  });
});
