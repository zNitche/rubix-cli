from rubix_cli.core import Commander
from rubix_cli.core import commands
from rubix_cli.core.cli import CliCommandBase


class LsCliCommand(CliCommandBase):
    def __init__(self, commander: Commander):
        cli_invoker = "ls"
        description = ""

        command = commands.LsCommand(commander)

        super().__init__(cli_invoker=cli_invoker, description=description,
                         command=command)


class CatReplCliCommand(CliCommandBase):
    def __init__(self, commander: Commander):
        cli_invoker = "cat_repl"
        description = ""
        command = commands.CatReplCommand(commander)

        super().__init__(cli_invoker=cli_invoker, command=command,
                         description=description)


class RebootCliCommand(CliCommandBase):
    def __init__(self, commander: Commander):
        cli_invoker = "reboot"
        description = ""

        command = commands.RebootCommand(commander)

        super().__init__(cli_invoker=cli_invoker, description=description,
                         command=command)


class FlashCliCommand(CliCommandBase):
    def __init__(self, commander: Commander):
        cli_invoker = "flash"
        description = ""

        command = commands.FlashCommand(commander)

        super().__init__(cli_invoker=cli_invoker, description=description,
                         command=command)


class CatCliCommand(CliCommandBase):
    def __init__(self, commander: Commander):
        cli_invoker = "cat"
        description = ""

        command = commands.CatCommand(commander)

        super().__init__(cli_invoker=cli_invoker, description=description,
                         command=command)


class GetRtcCliCommand(CliCommandBase):
    def __init__(self, commander: Commander):
        cli_invoker = "get_rtc"
        description = ""

        command = commands.GetRtcCommand(commander)

        super().__init__(cli_invoker=cli_invoker, description=description,
                         command=command)


class MkDirCliCommand(CliCommandBase):
    def __init__(self, commander: Commander):
        cli_invoker = "mkdir"
        description = ""

        command = commands.MkDirCommand(commander)

        super().__init__(cli_invoker=cli_invoker, description=description,
                         command=command)


class PurgeCliCommand(CliCommandBase):
    def __init__(self, commander: Commander):
        cli_invoker = "purge"
        description = ""

        command = commands.PurgeCommand(commander)

        super().__init__(cli_invoker=cli_invoker, description=description,
                         command=command)


class RmCliCommand(CliCommandBase):
    def __init__(self, commander: Commander):
        cli_invoker = "rm"
        description = ""

        command = commands.RmCommand(commander)

        super().__init__(cli_invoker=cli_invoker, description=description,
                         command=command)


class RmDirCliCommand(CliCommandBase):
    def __init__(self, commander: Commander):
        cli_invoker = "rmdir"
        description = ""

        command = commands.RmDirCommand(commander)

        super().__init__(cli_invoker=cli_invoker, description=description,
                         command=command)


class SetRtcCliCommand(CliCommandBase):
    def __init__(self, commander: Commander):
        cli_invoker = "set_rtc"
        description = ""

        command = commands.SetRtcCommand(commander)

        super().__init__(cli_invoker=cli_invoker, description=description,
                         command=command)


class UnameCliCommand(CliCommandBase):
    def __init__(self, commander: Commander):
        cli_invoker = "uname"
        description = ""

        command = commands.UnameCommand(commander)

        super().__init__(cli_invoker=cli_invoker, description=description,
                         command=command)


class UploadFileCliCommand(CliCommandBase):
    def __init__(self, commander: Commander):
        cli_invoker = "upload"
        description = ""

        command = commands.UploadFileCommand(commander)

        super().__init__(cli_invoker=cli_invoker, description=description,
                         command=command)
