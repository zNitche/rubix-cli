from rubix_cli.core import Commander


class CommandBase:
    def __init__(self, commander: Commander):
        self._commander = commander

    def exec(self):
        raise NotImplementedError()
