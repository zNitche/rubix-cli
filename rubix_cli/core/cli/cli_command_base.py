import inspect
from collections.abc import Callable
from rubix_cli.core.commands import CommandBase


class CliCommandBase:
    def __init__(self, cli_invoker: str, command: CommandBase, description: str | None):
        self.cli_invoker = cli_invoker
        self.description = description

        self.command = command
        self.args: dict | None = self._get_func_args(self.command.exec)

    def _get_func_args(self, func: Callable):
        args = {}
        inspect_data = inspect.signature(func).parameters

        for key, val in inspect_data.items():
            args[key] = val.annotation.__name__

        return None if len(args.keys()) == 0 else args
