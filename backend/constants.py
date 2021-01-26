from enum import Enum
from Box2D import b2_dynamicBody, b2_kinematicBody, b2_staticBody
MatchState = Enum('MatchState', ['NOT_STARTED', 'STARTED', 'PAUSE', 'ENDED'])

LEFT = 'ArrowLeft'
RIGHT = 'ArrowRight'
UP = 'ArrowUp'


BOX2D_VEL_ITERS = 6
BOX2D_POS_ITERS = 2


class BodyType(int, Enum):
    STATIC = b2_staticBody
    KINEMATIC = b2_kinematicBody
    DYNAMIC = b2_dynamicBody
