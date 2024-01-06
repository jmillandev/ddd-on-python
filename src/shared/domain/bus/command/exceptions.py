from . import Command


class CommandNotRegistered(Exception):

    def __init__(self, command: Command) -> None:
        self.command = command
        super().__init__(f"Miising CommandHandler for <{command.__class__}>")
