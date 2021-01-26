from typing import Dict
import pytest
from unittest.mock import Mock, MagicMock, patch, call, ANY
import socketio
from socketio.packet import Packet
import server.custom_json as custom_json
from game.game import Game
import client_interfaces as ci
import server_interfaces as si
from server.server import Server
from repository import repository_factory
from systems import SYSTEMS
from Box2D import b2Vec2


@pytest.fixture
def eio():
    with patch('engineio.Server') as eio:
        eio.return_value.generate_id.side_effect = [f'player{i}' for i in range(1, 10)]
        yield eio


@pytest.fixture
def sio(eio):
    with patch.object(socketio.server.Server, 'start_background_task'):
        sio = socketio.server.Server(async_handlers=False, json=custom_json)
        sio.manager.initialize = MagicMock()
        with patch.object(sio, 'emit'):
            yield sio


@pytest.fixture
def game():
    game = Mock(wraps=Game(SYSTEMS, repository_factory))
    with patch('server.server.Game', return_value=game):
        yield game


@pytest.fixture
def server(sio, game):
    with patch('eventlet.wsgi.server'):
        server = Server(None, sio, game)
        sio.register_namespace(server)
        yield server


@pytest.fixture
def room_and_player(helper, game):
    helper.handle_connect()
    helper.handle_message('create_room', {"name": "foo", "private": False})
    game.create_room.assert_called_once_with('player1', ci.CreateRoomDTO(name='foo', private=False), ANY)


@pytest.fixture
def helper(sio):
    class Helper:
        def __init__(self, sio):
            self.sio = sio

        def handle_connect(self, sid: str = None):
            self.sio.manager.connect(sid or 'player1', '/')

        def handle_message(self, event_name: str, data: Dict, packet_type=2, sid: str = None, **kwargs):
            packet = Packet(packet_type, [event_name, data], namespace='/')
            self.sio._handle_eio_message(sid or 'player1', packet.encode())
    return Helper(sio)


class TestServerE2E:
    def test_create_room(self, sio, server, game, helper):
        helper.handle_connect()
        helper.handle_message('create_room', {"name": "foo", "private": False})
        game.create_room.assert_called_once_with('player1', ci.CreateRoomDTO(name='foo', private=False), ANY)

    def test_player_join(self, sio, server, game, helper, room_and_player):
        helper.handle_connect(sid='player2')
        helper.handle_message('join_room', {"room_id": "room0"}, sid='player2')

        game.join_room.assert_called_once()
        assert game.join_room.mock_calls[0].args[0] == 'player2'

        server.tick(sort=True)

        sio.emit.assert_has_calls(
            [
                call('long_sync', si.LongSyncDTO(updates=[
                    si.EntityData(
                        id='floor',
                        position=None,
                        velocity=None,
                        shape=None,
                        color=None),
                    si.EntityData(
                        id='player1',
                        position=b2Vec2(0, 0),
                        velocity=b2Vec2(0, 0),
                        shape=ANY,
                        color=ANY),
                    si.EntityData(
                        id='player2',
                        position=b2Vec2(0, 0),
                        velocity=b2Vec2(0, 0),
                        shape=ANY,
                        color=ANY),
                ]), 'room0')
            ], any_order=True)
