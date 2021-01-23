from unittest.mock import Mock, call, ANY
from server.server import Server


def fake_flag(set_after: int, initial_value=False, set_value=True):
    """Returns fake threading.Event"""
    fake_event = Mock()
    fake_event.is_set.side_effect = [initial_value] * set_after + [set_value]
    return fake_event


class TestServerSync:
    def test_sync_calls_2_per_second(self):
        game = Mock(name='game')
        server = Server(None, Mock(name='sio'), game)
        shutdown_flag = fake_flag(set_after=4)
        server.sync(shutdown_flag, ticks_per_second=2)

        assert len(game.method_calls) == 4
        game.assert_has_calls([
            call.update_long(ANY, False),
            call.update_short(ANY, ANY, False),
            call.update_long(ANY, False),
            call.update_short(ANY, ANY, False),
        ])

    def test_sync_calls_5_per_second(self):
        game = Mock(name='game')
        server = Server(None, Mock(name='sio'), game)
        shutdown_flag = fake_flag(set_after=5)
        server.sync(shutdown_flag, ticks_per_second=5)

        assert len(game.method_calls) == 5
        game.assert_has_calls([
            call.update_long(ANY, False),
            call.update_short(ANY, ANY, False),
            call.update_short(ANY, ANY, False),
            call.update_short(ANY, ANY, False),
            call.update_short(ANY, ANY, False)
        ])
