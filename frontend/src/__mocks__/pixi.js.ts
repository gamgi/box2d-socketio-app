import Pixi, { Ticker } from 'pixi.js';
import { mocked } from 'ts-jest/utils';

const ActualPIXI = jest.requireActual<typeof Pixi>('pixi.js');
const MockedPIXI = jest.createMockFromModule<typeof Pixi>('pixi.js');

export const {
  Graphics,
  Sprite,
  Texture,
  BaseTexture,
  utils,
  Rectangle,
  Text,
  TextStyle,
  RenderTexture,
  SCALE_MODES,
} = ActualPIXI;
export const { Container, TextMetrics, Loader } = MockedPIXI;

// eslint-disable-next-line @typescript-eslint/no-unsafe-return
mocked(TextMetrics.measureText).mockImplementation(() => ({ width: 100, height: 100 } as any));

mocked(Loader).shared = {
  reset: jest.fn(),
  add: jest.fn(),
  onError: { add: jest.fn() } as any,
  load: (callback: () => void) => callback(),
} as any;

const MockApplication = MockedPIXI.Application;

export class Application extends MockApplication {
  stage: Pixi.Container = new Container();
  screen = new Rectangle(0, 0, 800, 600);
  ticker = { add: jest.fn() as any } as jest.Mocked<Ticker>;
}

export default MockedPIXI;
