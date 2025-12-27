import os
from rubix_cli.core import SerialTTY
from rubix_cli.core.consts import MP_CONSTS
from rubix_cli.core.utils import Logger
from rubix_cli import snippets


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

    def __send_command(self, cmd: str):
        self.__logger.debug(f"sending: {cmd}")

        if self.__serial is None:
            raise Exception("interface has not been specified")

        raw_response = b""
        raw_error = b""

        self.__serial.soft_reboot()
        self.__serial.enter_raw_repl()

        try:
            raw_response, raw_error = self.__serial.send_command(data=cmd)

        except:
            self.__logger.exception("error while processing tty session")

        self.__serial.exit_raw_repl()

        response = self.__parse_command_response(raw_response)
        errors = self.__parse_command_response(raw_error)

        return response, errors

    def __handle_command_response(self, response: str, errors: str | None):
        if errors:
            self.__logger.exception(errors)
            return

        res = "OK" if not response else response
        self.__logger.info(res)

    def __default_cmd_handler(self, cmd: str):
        data, errors = self.__send_command(cmd)
        self.__handle_command_response(data, errors)

    def ls(self, path: str = "/"):
        self.__logger.info(f"ls at '{path}'")

        cmd = snippets.SnippetLs().get_code({"path": path})
        self.__default_cmd_handler(cmd)

    def rm(self, path: str):
        self.__logger.info(f"rm '{path}'")

        cmd = snippets.SnippetRm().get_code({"path": path})
        self.__default_cmd_handler(cmd)

    def rmdir(self, path: str):
        self.__logger.info(f"rmdir '{path}'")

        cmd = snippets.SnippetRmDir().get_code({"path": path})
        self.__default_cmd_handler(cmd)

    def purge(self):
        self.__logger.info(f"purge")

        cmd = snippets.SnippetPurge().get_code({})
        self.__default_cmd_handler(cmd)

    def mkdir(self, path: str):
        self.__logger.info(f"mkdir '{path}'")

        cmd = snippets.SnippetMkDir().get_code({"path": path})
        self.__default_cmd_handler(cmd)

    def set_rtc(self):
        self.__logger.info("setting rtc")

        cmd = snippets.SnippetSetRtc().get_code()
        self.__default_cmd_handler(cmd)

    def get_rtc(self):
        self.__logger.info("getting rtc")

        cmd = snippets.SnippetGetRtc().get_code()
        self.__default_cmd_handler(cmd)

    def uname(self):
        self.__logger.info("uname")

        cmd = snippets.SnippetUname().get_code()
        self.__default_cmd_handler(cmd)

    def upload_file(self, source_path: str, target_path: str):
        self.__logger.info(f"uploading {source_path} -> {target_path}")

        if not os.path.exists(source_path):
            raise Exception(f"'{source_path}' doesn't exist")

        with open(source_path, "rb") as file:
            file_content = file.read()

        cmd = snippets.SnippetUploadFile().get_code(
            {"file_content": file_content, "file_path": target_path})

        self.__default_cmd_handler(cmd)

    def get_file(self, path: str):
        self.__logger.info("uname")

        cmd = snippets.SnippetGetFile().get_code({"path": path})

        self.__default_cmd_handler(cmd)
