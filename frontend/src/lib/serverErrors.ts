/* eslint-disable max-classes-per-file */

export class ServerError extends Error {
  public userMessage: string;
  public userDescription: string | null;
  public code: number;

  constructor(message: string, userMessage?: string, userDescription?: string, code?: number) {
    super(message);
    this.userMessage = userMessage ?? 'Unknown error';
    this.userDescription = userDescription ?? null;
    this.code = code ?? 500;
  }
}
