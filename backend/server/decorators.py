import logging
from functools import wraps
import server_interfaces as server
from game.exc import GameError


def returns_error_dto(fun):
    @wraps(fun)
    def decorated(*args, **kwargs):
        try:
            return fun(*args, **kwargs)
        except GameError as err:
            logging.error(err)
            return server.ErrorDTO(True, err.code, err.message or 'Unknown error')
        except TypeError as err:
            logging.error(err, exc_info=True)
            message = getattr(err, 'message', str(err))
            return server.ErrorDTO(True, 400, message or 'Unknown error')
        except Exception as err:
            logging.error(err, exc_info=True)
    return decorated
