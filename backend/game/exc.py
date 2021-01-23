from typing import Optional


class GameError(Exception):
    default_code: int = 500

    def __init__(self, message: str, code: Optional[int] = None):
        super().__init__(message)
        self.message = message
        self.code = code or self.default_code
