import enum


class Pronoun(str, enum.Enum):
    HE = 'he'
    SHE = 'she'

    @staticmethod
    def keys():
        return [c.value for c in Pronoun]
