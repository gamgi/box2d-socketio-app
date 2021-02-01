import { Application, Container, Graphics, Text, TextStyle, TextMetrics } from 'pixi.js';

const UI_MARGIN = 200;
const TEXT_MARGIN = 20;

export enum MessageLevel {
  INFO = 0,
  ERROR = 1,
}

const PREFIX: Record<MessageLevel, string> = {
  [MessageLevel.INFO]: '',
  [MessageLevel.ERROR]: '⚠ error: ',
};

export class Ui {
  public stage: Container = new Container();
  private notification = new Graphics();
  private textStyle: TextStyle;
  private screen: { width: number; height: number };
  private debug = new Graphics();
  private debugData: Record<string, string> = {};

  constructor(private pixi: Application) {
    pixi.stage.addChild(this.stage);
    this.screen = { width: pixi.screen.width, height: pixi.screen.height };
    this.textStyle = new TextStyle({
      wordWrap: true,
      wordWrapWidth: this.screen.width - UI_MARGIN * 2 - TEXT_MARGIN * 2,
    });
  }

  public clearMessage(): void {
    this.notification.clear();
    this.notification.removeChildren();
    this.stage.removeChild(this.notification);
  }

  public showMessage(message: string, level: MessageLevel = MessageLevel.INFO): void {
    this.clearMessage();
    const fullMessage = PREFIX[level] + message;
    const center = { x: this.screen.width / 2, y: this.screen.height / 2 };
    const textMetrics = TextMetrics.measureText(fullMessage, this.textStyle);
    const { width, height } = textMetrics;
    this.notification.beginFill(0xdeccaa);
    this.notification.lineStyle(5, 0x8b7956);
    this.notification.drawRect(
      center.x - width / 2 - TEXT_MARGIN,
      center.y - height / 2 - TEXT_MARGIN,
      width + TEXT_MARGIN * 2,
      height + TEXT_MARGIN * 2,
    );

    const text = new Text(fullMessage, this.textStyle);
    text.anchor.set(0.5, 0.5);
    text.position.set(center.x, center.y);
    this.notification.addChild(text);
    this.stage.addChild(this.notification);
  }

  public updateDebugVariable(name: string, value: string): void {
    if (this.debug.children.length === 0) {
      const text = new Text(JSON.stringify(this.debugData, null, 2), {
        ...this.textStyle,
        fill: 0xffffff,
        fontSize: 20,
      });
      this.debug.addChild(text);
      this.stage.addChild(this.debug);
    } else {
      this.debugData[name] = value;
      (this.debug.children[0] as Text).text = JSON.stringify(this.debugData, null, 2);
    }
  }
}
