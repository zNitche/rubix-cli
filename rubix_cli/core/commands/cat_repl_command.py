from rubix_cli.core.commands import CommandBase


class CatReplCommand(CommandBase):
    def exec(self):
        self._commander.listen_on_repl()
