from enum import Enum
from Box2D import b2_dynamicBody, b2_kinematicBody, b2_staticBody
MatchState = Enum('MatchState', ['NOT_STARTED', 'STARTED', 'PAUSE', 'ENDED'])

LEFT = 'ArrowLeft'
RIGHT = 'ArrowRight'
UP = 'ArrowUp'


BOX2D_VEL_ITERS = 25
BOX2D_POS_ITERS = 50


class BodyType(int, Enum):
    STATIC = b2_staticBody
    KINEMATIC = b2_kinematicBody
    DYNAMIC = b2_dynamicBody
