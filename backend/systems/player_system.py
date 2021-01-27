import logging
from typing import List, Dict
from ecs.base_system import System
from ecs.context import Context
from collections import defaultdict
import client_interfaces as ci
from components import Box2DBody, Box2DWorld, Position, Velocity, Collidable
from components import Player, Match, Team, Input
from constants import LEFT, RIGHT, UP


class PlayerSystem(System):
    def __init__(self, context: Context):
        self.context = context

    def on_player_join(self, sid: str):
        self._spawn_player(sid)
        self._assign_team(sid)
        logging.info('spawned')

    def on_player_leave(self, sid: str):
        self._remove_player(sid)

    def on_input(self, sid: str, data: ci.InputDTO):
        move_left = LEFT in data.keys_down
        move_right = RIGHT in data.keys_down

        input_ = Input(
            move_left=move_left and not move_right,
            move_right=move_right and not move_left,
            jump=UP in data.keys_down
        )

        self.context.upsert(sid, input_)

    def _spawn_player(self, entity_id: str):
        world = self._get_world()

        player_body = world.CreateDynamicBody(position=(0, 0))
        player_body.CreatePolygonFixture(box=(1, 1), density=1, friction=0.3)
        body = Box2DBody(player_body)

        position = Position.from_body(player_body)
        velocity = Velocity.from_body(player_body)
        player = Player(color=int('0xff0000', 16))
        collidable = Collidable()

        self.context.upsert(
            entity_id,
            body,
            position,
            velocity,
            player,
            collidable
        )

    def _remove_player(self, entity_id: str):
        world = self._get_world()
        body = self.context.component(entity_id, Box2DBody)
        if body:
            world.DestroyBody(body.body)  # type:ignore

    def _assign_team(self, entity_id: str):
        teams = self._get_teams_player_count()
        team_with_min_players = min(teams, key=teams.get)  # type:ignore

        team = Team(team_with_min_players)
        self.context.upsert(entity_id, team)

    def _get_teams_player_count(self) -> Dict[int, int]:
        entities = self.context.get_entities_with(Team, Player)
        teams = self._get_teams()

        # default to existing teams (but allow more teams to exist)
        player_count: Dict[int, int] = defaultdict(int, {team: 0 for team in teams})
        for entity_id in entities:
            team = self.context.component(entity_id, Team)
            player_count[team.index] += 1  # type: ignore
        return player_count

    def _get_world(self):
        return self.context.singleton(Box2DWorld, field='world')

    def _get_teams(self) -> List[int]:
        return self.context.singleton(Match, field='teams')  # type: ignore
