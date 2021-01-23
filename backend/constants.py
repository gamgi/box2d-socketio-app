from enum import Enum

MatchState = Enum('MatchState', ['NOT_STARTED', 'STARTED', 'PAUSE', 'ENDED'])

LEFT = 'ArrowLeft'
RIGHT = 'ArrowRight'
UP = 'ArrowUp'


BOX2D_VEL_ITERS = 6
BOX2D_POS_ITERS = 2
