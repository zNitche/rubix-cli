import os
from rubix_cli.core.commands import CommandBase
from rubix_cli.snippets import filesystem_snippets, flash_snippets


class FlashCommand(CommandBase):
    def exec(self, root_path: str = ""):
        if not root_path:
            raise Exception("path can't be empty")

        self._commander._logger.info(f"flashing '{root_path}'")

        if os.path.isfile(root_path):
            raise Exception(f"{root_path} should point to directory")

        self._commander._logger.info("purging...")

        cmd = filesystem_snippets.SnippetPurge().get_code()
        self._commander.default_cmd_handler(cmd)

        self._commander.soft_reboot()

        flash_snippet = flash_snippets.SnippetFlash()
        self._commander._logger.info(message="purged, flashing...")

        for (dirpath, dirnames, filenames) in os.walk(root_path):
            root = dirpath.replace(root_path, "")

            for dirname in dirnames:
                path = f"{root}/{dirname}"
                self._commander._logger.info(
                    message=f"creating {path} directory...")

                cmd = flash_snippet.get_code(
                    {"dirname": dirname, "path": path})
                self._commander.default_cmd_handler(
                    cmd, reboot=False, raise_exception_on_errors=True)

            for filename in filenames:
                with open(os.path.join(dirpath, filename), "rb") as file:
                    content = file.read()

                path = f"{root}/{filename}"
                self._commander._logger.info(message=f"flashing {path}...")

                cmd = flash_snippet.get_code(
                    {"filename": filename, "file_content": content, "path": path})

                self._commander.default_cmd_handler(
                    cmd, reboot=False, raise_exception_on_errors=True)
