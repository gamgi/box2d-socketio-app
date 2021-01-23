import pytest
from unittest.mock import Mock, patch
from game.exc import GameError
from game.game import Game
from ecs.base_system import ExternalEvent
from components import Position, Box2DBody
import server_interfaces as si
import client_interfaces as ci


class TestGame:
    sid = '123abc'

    def test_get_rooms(self):
        game = Game([], dict)

        response = game.get_rooms()
        assert response == si.GetRoomsDTO(rooms=[])

        game.create_room('player1', ci.CreateRoomDTO(name='my room', private=False), Mock())
        game.create_room('player2', ci.CreateRoomDTO(name='my private room', private=True), Mock())

        response = game.get_rooms()
        assert response.rooms == [si.RoomMeta(
            id='room0',
            name='my room',
            players=['player1'],
            max_players=4,
            private=False,
            level='beach'
        )]

    def test_create_room_initializes_context_and_systems(self):
        mock_system = Mock(spec=[])
        mock_repository_factory = Mock(return_value={})
        game = Game([mock_system], mock_repository_factory)

        with patch('game.game.Context') as mock_context:
            game.create_room(self.sid, ci.CreateRoomDTO('my room', private=False), Mock())

        mock_repository_factory.assert_called_with()
        mock_context.assert_called_with(repository=mock_repository_factory.return_value)
        mock_system.assert_called_with(mock_context.return_value)

    def test_create_room_calls_callback(self):
        game = Game([], dict)
        callback = Mock()
        room_id = game.create_room(self.sid, ci.CreateRoomDTO('my room', private=False), callback).room.id

        callback.assert_called_with(room_id)

    def test_join_room(self):
        game = Game([], dict)
        game.create_room(self.sid, ci.CreateRoomDTO(name='my room', private=False), Mock())

        response = game.get_rooms()
        assert response.rooms == [si.RoomMeta(
            id='room0',
            name='my room',
            players=[self.sid],
            max_players=4,
            private=False,
            level='beach'
        )]

    def test_join_room_calls_callback(self):
        game = Game([], dict)
        callback = Mock()

        room_id = game.create_room(self.sid, ci.CreateRoomDTO(name='my room', private=False), callback).room.id
        callback.assert_called_once_with(room_id)

    def test_join_nonexistent_room_raises(self):
        game = Game([], dict)

        with pytest.raises(GameError, match='Room does not exist'):
            game.join_room(self.sid, ci.JoinRoomDTO(room_id='nonexistent'), Mock())

    def test_create_room_twice_raises(self):
        game = Game([], dict)

        game.create_room(self.sid, ci.CreateRoomDTO(name='my room 1', private=False), Mock())
        with pytest.raises(GameError, match='You are already in a room'):
            game.create_room(self.sid, ci.CreateRoomDTO(name='my room 2', private=False), Mock())

    def test_join_room_twice_raises(self):
        game = Game([], dict)

        room_id = game.create_room('player2', ci.CreateRoomDTO(name='my room 1', private=False), Mock()).room.id

        game.create_room(self.sid, ci.CreateRoomDTO(name='my room 2', private=False), Mock())
        with pytest.raises(GameError, match='You are already in a room'):
            game.join_room(self.sid, ci.JoinRoomDTO(room_id=room_id), Mock())

    def test_trigger_event(self):
        mock_system = Mock(spec=['on_update'], name='system')
        game = Game([mock_system], dict)
        room_id = game.create_room('player1', ci.CreateRoomDTO(name='my room', private=False), Mock()).room.id

        game.trigger_event(ExternalEvent.UPDATE, room_id)
        mock_system.return_value.on_update.assert_called_once()

    def test_update_short(self):
        game = Game([Mock(spec=[])])
        room_id = game.create_room(self.sid, ci.CreateRoomDTO(name='my room 1', private=False), Mock()).room.id
        callback = Mock()

        game.update_short(1, callback)
        callback.assert_called_once_with(si.ShortSyncDTO(updates=[]), room_id)
        callback.reset_mock()

        game.contexts['room0'].upsert('0', Position.at([0, 0]))
        game.update_short(1, callback)
        updates = callback.call_args_list[0][0][0].updates
        assert updates == [si.ShortEntityData(id='0', position=(0.0, 0.0), velocity=None)]

    def test_update_short_does_not_reset_other_components_updates(self):
        body = Mock(awake=True, position=(1, 2), fixtures=[])
        game = Game([Mock(spec=[])])
        game.create_room(self.sid, ci.CreateRoomDTO(name='my room 1', private=False), Mock())

        game.contexts['room0'].upsert('0', Position.at([0, 0]), Box2DBody(body))

        game.update_short(1, Mock())
        assert game.contexts['room0'].get_all_updated_entities() == {'0'}

    def test_update_long(self):
        body = Mock(awake=True, position=(1, 2), fixtures=[])
        game = Game([Mock(spec=[])])
        game.create_room(self.sid, ci.CreateRoomDTO(name='my room 1', private=False), Mock())
        callback = Mock()

        game.contexts['room0'].upsert('0', Box2DBody(body))
        game.update_short(1, Mock())
        game.update_long(callback)

        updates = callback.call_args_list[0][0][0].updates
        assert updates == [si.EntityData(
            id='0',
            position=None,
            velocity=None,
            shape=None
        )]
