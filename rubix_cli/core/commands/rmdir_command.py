from rubix_cli.core.commands import CommandBase
from rubix_cli.snippets import filesystem_snippets


class RmDirCommand(CommandBase):
    def exec(self, path: str = ""):
        if not path:
            raise Exception("path can't be empty")

        self._commander._logger.info(f"rmdir '{path}'")

        cmd = filesystem_snippets.SnippetRmDir().get_code({"path": path})
        self._commander.default_cmd_handler(cmd)
