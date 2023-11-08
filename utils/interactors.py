from utils.errors import BaseError as Error


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
