from enum import Enum

MatchState = Enum('MatchState', ['NOT_STARTED', 'STARTED', 'PAUSE', 'ENDED'])
LEFT = 'ArrowLeft'
RIGHT = 'ArrowRight'
UP = 'ArrowUp'
