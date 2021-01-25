/* eslint-disable max-classes-per-file */

export class ClientError extends Error {
  public userMessage: string;
  public userDescription: string | null;

  constructor(message: string, userMessage?: string, userDescription?: string) {
    super(message);
    this.userMessage = userMessage ?? 'Unknown error';
    this.userDescription = userDescription ?? null;
  }
}

export class ConnectionError extends ClientError {
  constructor(message: string, userMessage = 'Failed to connect to server', userDescription?: string) {
    super(message, userMessage, userDescription);
  }
}
