import os
import re
from rubix_cli.core.commands import CommandBase
from rubix_cli.snippets import filesystem_snippets, flash_snippets


class FlashCommand(CommandBase):
    def __read_flashignore(self, root_path: str):
        expressions: list[re.Pattern[str]] = []
        flashignore_path = os.path.join(root_path, ".flashignore")

        if os.path.exists(flashignore_path):
            self._commander._logger.info("found .flashignore, loading...")

            with open(flashignore_path, "r") as file:
                content = file.readlines()

                for line in content:
                    exp = re.compile(line.rstrip())
                    expressions.append(exp)

            self._commander._logger.info(
                f".flashignore has been loaded, found {len(expressions)} rules")
            
            expressions.append(re.compile(r"^/.flashignore"))

        return expressions

    def __check_if_should_be_ignored(self, path: str, expressions: list[re.Pattern[str]]):
        for exp in expressions:
            if exp.search(path) is not None:
                return True

        return False

    def __purge(self):
        self._commander._logger.info("purging...")

        cmd = filesystem_snippets.SnippetPurge().get_code()
        self._commander.default_cmd_handler(cmd)

        self._commander.soft_reboot()

    def __flash_object(self, flash_snippet: flash_snippets.SnippetFlash,
                       filename: str = "", file_content: bytes = b"",
                       path: str = "", dirname: str = ""):

        if file_content:
            self._commander._logger.info(message=f"flashing {path}...")
        else:
            self._commander._logger.info(
                message=f"creating {path} directory...")

        cmd = flash_snippet.get_code(
            {"filename": filename, "dirname": dirname,
             "file_content": file_content, "path": path})

        self._commander.default_cmd_handler(
            cmd, reboot=False, raise_exception_on_errors=True)

    def exec(self, root_path: str = ""):
        if not root_path:
            raise Exception("path can't be empty")

        self._commander._logger.info(f"flashing '{root_path}'")

        if os.path.isfile(root_path):
            raise Exception(f"{root_path} should point to directory")

        self.__purge()

        flash_snippet = flash_snippets.SnippetFlash()
        self._commander._logger.info(message="purged, flashing...")

        flashignore_exp = self.__read_flashignore(root_path)

        for (dirpath, dirnames, filenames) in os.walk(root_path):
            root = dirpath.replace(root_path, "")

            if self.__check_if_should_be_ignored(root, flashignore_exp):
                continue

            for dirname in dirnames:
                path = f"{root}/{dirname}"

                if not self.__check_if_should_be_ignored(path, flashignore_exp):
                    self.__flash_object(
                        flash_snippet, dirname=dirname, path=path)

            for filename in filenames:
                with open(os.path.join(dirpath, filename), "rb") as file:
                    content = file.read()

                path = f"{root}/{filename}"

                if not self.__check_if_should_be_ignored(path, flashignore_exp):
                    self.__flash_object(
                        flash_snippet, filename=filename, file_content=content, path=path)
