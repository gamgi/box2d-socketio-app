import logging
import eventlet
import socketio
import server.custom_json as custom_json
from server.server import Server
from game.game import Game
from systems import SYSTEMS
from repository import repository_factory
from constants import CORS_ALLOWED_ORIGINS, ASSET_FILES
logging.basicConfig(level=logging.INFO)


def main():
    logging.info('server started')
    eventlet.monkey_patch()
    sio = socketio.Server(
        async_mode='eventlet',
        json=custom_json,
        cors_allowed_origins=CORS_ALLOWED_ORIGINS)
    try:
        app = socketio.WSGIApp(sio, static_files={
            '/': '../frontend/build/index.html',
            '/bundle.js': '../frontend/build/bundle.js',
            '/static': '../frontend/build',
            **ASSET_FILES
        })
        game = Game(SYSTEMS, repository_factory)

        Server.serve(sio, app, game)
    finally:
        logging.error('stopped')
        sio.eio.disconnect()


if __name__ == '__main__':
    main()
