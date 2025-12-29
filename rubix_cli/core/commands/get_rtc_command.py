from rubix_cli.core.commands import CommandBase
from rubix_cli.snippets import system_snippets


class GetRtcCommand(CommandBase):
    def exec(self):
        self._commander._logger.info("getting rtc")

        cmd = system_snippets.SnippetGetRtc().get_code()
        self._commander.default_cmd_handler(cmd)
