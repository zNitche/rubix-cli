import os
from rubix_cli.core import SerialTTY
from rubix_cli.core.consts import MP_CONSTS
from rubix_cli.core.utils import Logger
from rubix_cli.snippets import filesystem_snippets, flash_snippets, system_snippets


class Commander:
    def __init__(self, interface: str | None, debug: bool = False,
                 timeout: int = 2, baudrate: int = 115200,
                 write_buffer_size: int = 128):

        self.__serial = self.__setup_serial_tty(interface, debug, timeout,
                                                baudrate, write_buffer_size)

        self.__logger = Logger(logger_name="rubix-cli")
        self.__logger.init(debug=debug)

    def __setup_serial_tty(self, interface: str | None, debug: bool, timeout: int,
                           baudrate: int, write_buffer_size: int):
        if not interface:
            return None

        return SerialTTY(
            interface=interface, debug=debug, timeout=timeout,
            baudrate=baudrate, write_buffer_size=write_buffer_size)

    def __parse_command_response(self, response: bytes):
        decoded_response = response.decode()

        subs_to_replace = [
            (MP_CONSTS.EOT_HEX.decode(), ""),
        ]

        for it in subs_to_replace:
            decoded_response = decoded_response.replace(it[0], it[1])

        return decoded_response

    def __send_command(self, cmd: str, reboot: bool = True):
        self.__logger.debug(f"sending: {cmd}")

        if self.__serial is None:
            raise Exception("interface has not been specified")

        raw_response = b""
        raw_error = b""

        if reboot:
            self.__logger.debug(message="soft reboot")

            self.__serial.soft_reboot()
            self.__serial.enter_raw_repl()

        try:
            raw_response, raw_error = self.__serial.send_command(data=cmd)

        except Exception as e:
            self.__logger.exception("error while processing tty session")
            raise e

        if reboot:
            self.__serial.exit_raw_repl()

        response = self.__parse_command_response(raw_response)
        errors = self.__parse_command_response(raw_error)

        return response, errors

    def __handle_command_response(self, response: str, errors: str | None, raise_exception_on_errors: bool = False):
        if errors:
            self.__logger.exception(errors)

            if raise_exception_on_errors:
                raise Exception("command returned some errors")

            return

        if response:
            self.__logger.info(response)

    def __default_cmd_handler(self, cmd: str, reboot: bool = True, raise_exception_on_errors: bool = False):
        data, errors = self.__send_command(cmd, reboot=reboot)
        self.__handle_command_response(data, errors, raise_exception_on_errors)

    def ls(self, path: str = "/"):
        self.__logger.info(f"ls at '{path}'")

        cmd = filesystem_snippets.SnippetLs().get_code({"path": path})
        self.__default_cmd_handler(cmd)

    def rm(self, path: str):
        self.__logger.info(f"rm '{path}'")

        cmd = filesystem_snippets.SnippetRm().get_code({"path": path})
        self.__default_cmd_handler(cmd)

    def rmdir(self, path: str):
        self.__logger.info(f"rmdir '{path}'")

        cmd = filesystem_snippets.SnippetRmDir().get_code({"path": path})
        self.__default_cmd_handler(cmd)

    def purge(self):
        self.__logger.info(f"purge")

        cmd = filesystem_snippets.SnippetPurge().get_code({})
        self.__default_cmd_handler(cmd)

    def mkdir(self, path: str):
        self.__logger.info(f"mkdir '{path}'")

        cmd = filesystem_snippets.SnippetMkDir().get_code({"path": path})
        self.__default_cmd_handler(cmd)

    def set_rtc(self):
        self.__logger.info("setting rtc")

        cmd = system_snippets.SnippetSetRtc().get_code()
        self.__default_cmd_handler(cmd)

    def get_rtc(self):
        self.__logger.info("getting rtc")

        cmd = system_snippets.SnippetGetRtc().get_code()
        self.__default_cmd_handler(cmd)

    def uname(self):
        self.__logger.info("uname")

        cmd = system_snippets.SnippetUname().get_code()
        self.__default_cmd_handler(cmd)

    def upload_file(self, source_path: str, target_path: str):
        self.__logger.info(f"uploading {source_path} -> {target_path}")

        if not os.path.exists(source_path):
            raise Exception(f"'{source_path}' doesn't exist")

        with open(source_path, "rb") as file:
            file_content = file.read()

        cmd = filesystem_snippets.SnippetUploadFile().get_code(
            {"file_content": file_content, "file_path": target_path})

        self.__default_cmd_handler(cmd)

    def get_file(self, path: str):
        self.__logger.info("uname")

        cmd = filesystem_snippets.SnippetGetFile().get_code({"path": path})

        self.__default_cmd_handler(cmd)

    def flash(self, root_path: str):
        self.__logger.info(f"flashing '{root_path}'")

        if os.path.isfile(root_path):
            raise Exception(f"{root_path} should point to directory")

        self.__logger.info("purging...")

        cmd = filesystem_snippets.SnippetPurge().get_code()
        self.__default_cmd_handler(cmd)

        flash_snippet = flash_snippets.SnippetFlash()
        self.__logger.info(message="purged, flashing...")

        for (dirpath, dirnames, filenames) in os.walk(root_path):
            root = dirpath.replace(root_path, "")

            for dirname in dirnames:
                path = f"{root}/{dirname}"
                self.__logger.info(message=f"creating {path} directory...")

                cmd = flash_snippet.get_code(
                    {"dirname": dirname, "filename": "", "file_content": b"", "path": path})
                self.__default_cmd_handler(cmd, reboot=True, raise_exception_on_errors=True)

            for filename in filenames:
                with open(os.path.join(dirpath, filename), "rb") as file:
                    content = file.read()

                path = f"{root}/{filename}"
                self.__logger.info(message=f"flashing {path}...")

                cmd = flash_snippet.get_code(
                    {"dirname": "", "filename": filename, "file_content": content, "path": path})
                
                self.__default_cmd_handler(cmd, reboot=True, raise_exception_on_errors=True)
