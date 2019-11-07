class YahooError(Exception):
    def __init__(self, message):
        self.message = message


class AccessDeniedException(YahooError):
    pass
