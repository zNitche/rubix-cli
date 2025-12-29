from rubix_cli.core.commands import CommandBase
from rubix_cli.snippets import system_snippets


class UnameCommand(CommandBase):
    def exec(self):
        self._commander._logger.info("uname")

        cmd = system_snippets.SnippetUname().get_code()
        self._commander.default_cmd_handler(cmd)
