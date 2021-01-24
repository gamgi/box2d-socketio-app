import logging
import eventlet
import socketio
import server.custom_json as custom_json
from server.server import Server
from game.game import Game
from systems import SYSTEMS
from repository import repository_factory

logging.basicConfig(level=logging.INFO)


def main():
    eventlet.monkey_patch()
    sio = socketio.Server(json=custom_json, cors_allowed_origins=['*', 'http://localhost:9000'])
    try:
        app = socketio.WSGIApp(sio, static_files={
            '/': '../frontend/build/index.html',
            '/assets': '../frontend/src/assets',
        })
        game = Game(SYSTEMS, repository_factory)

        Server.serve(sio, app, game)
    finally:
        logging.error('stopped')
        sio.eio.disconnect()


if __name__ == '__main__':
    main()
