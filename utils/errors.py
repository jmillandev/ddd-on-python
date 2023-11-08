class BaseError(Exception):
    def __init__(self, status_code: int, message: str, source: str):
        self.status_code = status_code
        self.message = message
        self.source = source

    def __iter__(self):
        yield 'status_code', self.status_code
        yield 'msg', self.message
        yield 'source', self.source

    def __str__(self):
        return self.message

    def __repr__(self):
        return f'<Error: {self.status_code} {self.message}>'
