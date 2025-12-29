from rubix_cli.core.commands import CommandBase
from rubix_cli.snippets import filesystem_snippets


class PurgeCommand(CommandBase):
    def exec(self):
        self._commander._logger.info(f"purge")

        cmd = filesystem_snippets.SnippetPurge().get_code()
        self._commander.default_cmd_handler(cmd)
