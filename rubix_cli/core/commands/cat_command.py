from rubix_cli.core.commands import CommandBase
from rubix_cli.snippets import filesystem_snippets


class CatCommand(CommandBase):
    def exec(self, path: str = ""):
        if not path:
            raise Exception("path can't be empty")

        self._commander._logger.info(f"cat {path}")

        cmd = filesystem_snippets.SnippetCatFile().get_code({"path": path})
        self._commander.default_cmd_handler(cmd)
