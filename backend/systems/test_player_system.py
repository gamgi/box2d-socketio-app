import pytest
from unittest.mock import Mock
from systems.player_system import PlayerSystem
import client_interfaces as ci
from components import Match, Team, Player, Input, Box2DWorld


@pytest.fixture
def context(empty_context):
    empty_context.new_singleton(Match.Default())
    empty_context.new_singleton(Box2DWorld(Mock()))
    return empty_context


@pytest.fixture
def system(context):
    system = PlayerSystem(context)
    return system


class TestPlayerSystem:
    def test_on_game_init_creates_player(self, system, context):
        system.on_player_join('player1')

        assert context.get_entities_with(Player) == {'player1'}
        assert context.component('player1', Player)
        assert context.component('player1', Team) == Team(index=0)

    def test_on_player_join_assigns_teams_evenly(self, system, context):
        system.on_player_join('player1')
        system.on_player_join('player2')
        system.on_player_join('player3')
        system.on_player_join('player4')

        assert context.get_entities_with(Team) == {'player1', 'player2', 'player3', 'player4'}
        assert context.component('player1', Team).index == 0
        assert context.component('player2', Team).index == 1
        assert context.component('player3', Team).index == 0
        assert context.component('player4', Team).index == 1

    def test_on_input_sets_input(self, system, context):
        system.on_player_join('player1')

        system.on_input('player1', ci.InputDTO(
            keys_down=['ArrowRight'],
            keys_pressed=None,
            keys_released=None)
        )
        assert context.component('player1', Input).move_right
        assert context.component('player1', Input).move_left is False
