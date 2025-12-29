import os
from rubix_cli.core.commands import CommandBase
from rubix_cli.snippets import filesystem_snippets


class UploadFileCommand(CommandBase):
    def exec(self, source_path: str = "", target_path: str = ""):
        if not source_path or not target_path:
            raise Exception("parh can't be empty")

        self._commander._logger.info(
            f"uploading {source_path} -> {target_path}")

        if not os.path.exists(source_path):
            raise Exception(f"'{source_path}' doesn't exist")

        with open(source_path, "rb") as file:
            file_content = file.read()

        cmd = filesystem_snippets.SnippetUploadFile().get_code(
            {"file_content": file_content, "file_path": target_path})

        self._commander.default_cmd_handler(cmd)
