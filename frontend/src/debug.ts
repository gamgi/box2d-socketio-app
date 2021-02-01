import { Ui } from './ui';
export class Debugger {
  private static instance: Debugger;
  private static ui: Ui | null = null;

  public static updateDebugVariable(name: string, value: string): void {
    if (this.ui) {
      this.ui.updateDebugVariable(name, value);
    }
  }

  public static init(ui: Ui): void {
    Debugger.ui = ui;
  }
}
