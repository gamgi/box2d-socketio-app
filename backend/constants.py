from enum import Enum
from Box2D import b2_dynamicBody, b2_kinematicBody, b2_staticBody
MatchState = Enum('MatchState', ['NOT_STARTED', 'STARTED', 'PAUSE', 'ENDED'])

LEFT = 'ArrowLeft'
RIGHT = 'ArrowRight'
UP = 'ArrowUp'
ENTER = 'Enter'


BOX2D_VEL_ITERS = 25
BOX2D_POS_ITERS = 50


class BodyType(int, Enum):
    STATIC = b2_staticBody
    KINEMATIC = b2_kinematicBody
    DYNAMIC = b2_dynamicBody


CORS_ALLOWED_ORIGINS = [
    'http://localhost:9000',
    'http://localhost:5000',
    'https://box2d-socketio-app.herokuapp.com']

ASSET_FILES = {
    '/assets/missing.svg': {'filename': '../frontend/src/assets/missing.svg', 'content_type': 'image/svg+xml'}
}
