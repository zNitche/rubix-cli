from rubix_cli.core import Commander
from rubix_cli.core import commands
from rubix_cli.core.cli import CliCommandBase


class LsCliCommand(CliCommandBase):
    def __init__(self, commander: Commander):
        cli_invoker = "ls"
        description = "list all files & directories at 'path'"

        command = commands.LsCommand(commander)

        super().__init__(cli_invoker=cli_invoker, description=description,
                         command=command)


class CatReplCliCommand(CliCommandBase):
    def __init__(self, commander: Commander):
        cli_invoker = "cat_repl"
        description = "preview stdout of MicroPython REPL"
        command = commands.CatReplCommand(commander)

        super().__init__(cli_invoker=cli_invoker, command=command,
                         description=description)


class RebootCliCommand(CliCommandBase):
    def __init__(self, commander: Commander):
        cli_invoker = "reboot"
        description = "reboot MCU"

        command = commands.RebootCommand(commander)

        super().__init__(cli_invoker=cli_invoker, description=description,
                         command=command)


class FlashCliCommand(CliCommandBase):
    def __init__(self, commander: Commander):
        cli_invoker = "flash"
        description = "upload content of 'root_path' to MCU root directory"

        command = commands.FlashCommand(commander)

        super().__init__(cli_invoker=cli_invoker, description=description,
                         command=command)


class CatCliCommand(CliCommandBase):
    def __init__(self, commander: Commander):
        cli_invoker = "cat"
        description = "preview file's specified by 'path' content"

        command = commands.CatCommand(commander)

        super().__init__(cli_invoker=cli_invoker, description=description,
                         command=command)


class GetRtcCliCommand(CliCommandBase):
    def __init__(self, commander: Commander):
        cli_invoker = "get_rtc"
        description = "get device RTC data"

        command = commands.GetRtcCommand(commander)

        super().__init__(cli_invoker=cli_invoker, description=description,
                         command=command)


class MkDirCliCommand(CliCommandBase):
    def __init__(self, commander: Commander):
        cli_invoker = "mkdir"
        description = "create directory at 'path'"

        command = commands.MkDirCommand(commander)

        super().__init__(cli_invoker=cli_invoker, description=description,
                         command=command)


class PurgeCliCommand(CliCommandBase):
    def __init__(self, commander: Commander):
        cli_invoker = "purge"
        description = "wipe files & directories stored on device"

        command = commands.PurgeCommand(commander)

        super().__init__(cli_invoker=cli_invoker, description=description,
                         command=command)


class RmCliCommand(CliCommandBase):
    def __init__(self, commander: Commander):
        cli_invoker = "rm"
        description = "remove file specified by 'path'"

        command = commands.RmCommand(commander)

        super().__init__(cli_invoker=cli_invoker, description=description,
                         command=command)


class RmDirCliCommand(CliCommandBase):
    def __init__(self, commander: Commander):
        cli_invoker = "rmdir"
        description = "remove directory specified by 'path'"

        command = commands.RmDirCommand(commander)

        super().__init__(cli_invoker=cli_invoker, description=description,
                         command=command)


class SetRtcCliCommand(CliCommandBase):
    def __init__(self, commander: Commander):
        cli_invoker = "set_rtc"
        description = "set MCU RTC to current date"

        command = commands.SetRtcCommand(commander)

        super().__init__(cli_invoker=cli_invoker, description=description,
                         command=command)


class UnameCliCommand(CliCommandBase):
    def __init__(self, commander: Commander):
        cli_invoker = "uname"
        description = "get MCU uname info"

        command = commands.UnameCommand(commander)

        super().__init__(cli_invoker=cli_invoker, description=description,
                         command=command)


class UploadFileCliCommand(CliCommandBase):
    def __init__(self, commander: Commander):
        cli_invoker = "upload"
        description = "upload file from 'source_path' to 'target_path' on MCU"

        command = commands.UploadFileCommand(commander)

        super().__init__(cli_invoker=cli_invoker, description=description,
                         command=command)
