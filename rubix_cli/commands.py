from rubix_cli.core import Commander
from rubix_cli.core.commands import LsCommand
from rubix_cli.core.cli import CliCommandBase


# class CliCatReplCommand(CliCommandBase):
#     def __init__(self, commander: Commander):
#         description = ""
#         func = commander.listen_on_repl

#         super().__init__(func=func, description=description)


class CliLsCommand(CliCommandBase):
    def __init__(self, commander: Commander):
        cli_invoker = "ls"
        description = ""

        command = LsCommand(commander)

        super().__init__(cli_invoker=cli_invoker, description=description,
                         command=command)
