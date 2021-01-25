import { Loader, IResourceDictionary } from 'pixi.js';

export function loadResources(paths: string[]): Promise<IResourceDictionary> {
  Loader.shared.reset();
  for (const path of paths) {
    const fileName = path.split('/').pop();
    Loader.shared.add(fileName, path);
  }

  return new Promise((resolve, reject) => {
    Loader.shared.onError.add(reject);
    Loader.shared.load(() => resolve(Loader.shared.resources));
  });
}
