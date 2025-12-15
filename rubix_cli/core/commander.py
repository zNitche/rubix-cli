from contextlib import contextmanager
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

    @contextmanager
    def __tty_session(self):
        if self.__serial is None:
            raise Exception("interface has not been specified")

        self.__serial.soft_reboot()
        self.__serial.enter_raw_repl()

        try:
            yield self.__serial

        except:
            self.__logger.exception("error while processing tty session")

        self.__serial.exit_raw_repl()

    def __parse_command_response(self, response: bytes):
        decoded_response = response.decode()

        subs_to_replace = [
            (MP_CONSTS.EOT_HEX.decode(), ""),
        ]

        for it in subs_to_replace:
            decoded_response = decoded_response.replace(it[0], it[1])

        return decoded_response

    def __send_command(self, cmd: str, serial_session: SerialTTY):
        self.__logger.debug(f"sending: {cmd}")

        raw_response, raw_error = serial_session.send_command(data=cmd)

        response = self.__parse_command_response(raw_response)
        errors = self.__parse_command_response(raw_error)

        return response, errors

    def __handle_command_response(self, response: str, errors: str | None):
        if errors:
            self.__logger.exception(errors)
            return
        
        res = "OK" if not response else response
        self.__logger.info(res)

    def ls(self, path: str = "/"):
        self.__logger.info(f"ls at '{path}'")

        with self.__tty_session() as session:
            cmd = snippets.SnippetLS().get_code({"path": path})

            data, errors = self.__send_command(cmd, session)
            self.__handle_command_response(data, errors)

    def rm(self, path: str):
        self.__logger.info(f"rm '{path}'")

        with self.__tty_session() as session:
            cmd = f"""
                import uos
                uos.remove("{path}")
            """

            data, errors = self.__send_command(cmd, session)
            self.__handle_command_response(data, errors)

    def rmdir(self, path: str):
        self.__logger.info(f"rmdir '{path}'")

        with self.__tty_session() as session:
            cmd = f"""
                import uos

                def rmdir(path):
                    uos.chdir(path)

                    for file in uos.listdir():
                        try:
                            uos.remove(file)
                            print("removed " + file)
                        except OSError:
                            pass
                            
                    for dir in uos.listdir():
                        rmdir(dir)
                        print("removed " + dir)

                    uos.chdir("..")
                    uos.rmdir(path)

                    print("removed " + path)

                rmdir("{path}")
            """

            data, errors = self.__send_command(cmd, session)
            self.__handle_command_response(data, errors)

    def purge(self):
        self.__logger.info(f"purge")

        with self.__tty_session() as session:
            cmd = f"""
                import uos

                def rmdir(path):
                    uos.chdir(path)

                    for file in uos.listdir():
                        try:
                            uos.remove(file)
                            print("removed " + file)
                        except OSError:
                            pass
                            
                    for dir in uos.listdir():
                        rmdir(dir)
                        print("removed " + dir)

                    uos.chdir("..")
                    uos.rmdir(path)

                    print("removed " + path)

                for file in uos.listdir():
                    rmdir(file)
            """

            data, errors = self.__send_command(cmd, session)
            self.__handle_command_response(data, errors)

    def mkdir(self, path: str):
        self.__logger.info(f"mkdir '{path}'")

        with self.__tty_session() as session:
            cmd = f"""
                import uos
                uos.mkdir("{path}")
            """

            data, errors = self.__send_command(cmd, session)
            self.__handle_command_response(data, errors)
