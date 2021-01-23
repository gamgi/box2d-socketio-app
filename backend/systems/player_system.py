from typing import List, Dict
from ecs.base_system import System
from ecs.context import Context
from collections import defaultdict
from components import Box2DBody, Box2DWorld, Position, Velocity
from components import Player, Match, Team


class PlayerSystem(System):
    def __init__(self, context: Context):
        self.context = context

    def on_player_join(self, sid: str):
        self._spawn_player(sid)
        self._assign_team(sid)

    def _spawn_player(self, entity_id: str):
        world = self._get_world()

        player_body = world.CreateDynamicBody(position=(0, 0))
        player_body.CreatePolygonFixture(box=(1, 1), density=1, friction=0.3)
        body = Box2DBody(player_body)

        position = Position.from_body(player_body)
        velocity = Velocity.from_body(player_body)
        player = Player(color='red')

        self.context.upsert(
            entity_id,
            body,
            position,
            velocity,
            player,
        )

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
            player_count[team.index] += 1
        return player_count

    def _get_world(self):
        return self.context.singleton(Box2DWorld, field='world')

    def _get_teams(self) -> List[int]:
        return self.context.singleton(Match, field='teams')
