UNKNOWN = "unknown"


class DomainException(Exception):
    def __init__(self, code: int, message: str, source: str = UNKNOWN):
        self.code = code
        self.message = message
        self.source = source or UNKNOWN

    def __iter__(self):
        yield "code", self.code
        yield "msg", self.message
        yield "source", self.source

    def __str__(self):
        return self.message

    def __repr__(self):
        return f"<Error: {self.code} {self.message}>"
