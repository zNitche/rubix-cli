from rubix_cli.core.commands import CommandBase
from rubix_cli.snippets import system_snippets


class SetRtcCommand(CommandBase):
    def exec(self):
        self._commander._logger.info("setting rtc")

        cmd = system_snippets.SnippetSetRtc().get_code()
        self._commander.default_cmd_handler(cmd)
