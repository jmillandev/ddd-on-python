class Error(Exception):
    def __init__(self, status_code: int, message: str, source: str):
        self.status_code = status_code
        self.message = message
        self.source = source

    def __iter__(self):
        yield 'status_code', self.status_code
        yield 'message', self.message
        yield 'source', self.source

    def __str__(self):
        return self.message

    def __repr__(self):
        return f'<Error: {self.status_code} {self.message}>'


class Context:

    def __init__(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])
            self._error = None

    @property
    def error(self):
        return self._error
    
    @error.setter
    def error(self, value: Error):
        self._error = value


class Interactor:

    @classmethod
    async def exec(cls, **kwargs) -> Context:
        instance = cls(**kwargs)
        try:
            await instance.call()
        except Error as e:
            instance.context.error = e
        return instance.context

    def __init__(self, **kwargs):
        self.context = Context(**kwargs)
        self._validated_data = None

    async def call(self):
        raise NotImplementedError()

    def fail(self, message: str, source: str = 'unknown', status_code: int = 400):
        raise Error(status_code=status_code, message=message, source=source)

    @property
    def validated_data(self):
        if not self._validated_data:
            self._validated_data = self.context.params.dict()

        return self._validated_data
