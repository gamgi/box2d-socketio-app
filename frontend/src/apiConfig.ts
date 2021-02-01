import { ClientOptions } from './lib';

export function getClientConfig(): ClientOptions {
  // eslint-disable-next-line @typescript-eslint/ban-ts-comment
  // @ts-ignore
  if (process.env.NODE_ENV === 'development') {
    // eslint-disable-next-line no-console
    console.info(`using developement backend`);
    return { url: 'http://localhost:5000' };
  } else {
    return { url: 'https://box2d-socketio-app.herokuapp.com' };
  }
}
