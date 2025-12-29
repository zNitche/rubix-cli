from rubix_cli.core.commander import Commander
from rubix_cli.core.commands import CommandBase
from rubix_cli.snippets import filesystem_snippets


class LsCommand(CommandBase):
    def exec(self, path: str = "/"):
        self._commander._logger.info(f"ls at '{path}'")

        cmd = filesystem_snippets.SnippetLs().get_code({"path": path})
        self._commander.default_cmd_handler(cmd)
