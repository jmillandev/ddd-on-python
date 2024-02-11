from kink import Container

from src.shared.infrastructure.dependency_injector import init


def test_should_be_one_alias_per_class():
    di = Container()

    init(di)

    for alias, clases in di._aliases.items():
        assert len(clases) == 1, f"Alias {alias} has more than one class"
