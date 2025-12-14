from contextlib import contextmanager
import textwrap
from rubix_cli.core import SerialTTY, MP_CONSTS
from rubix_cli.core.utils import Logger


class Commander:
    def __init__(self, interface: str, debug: bool = False):
        self.__serial = SerialTTY(interface=interface, debug=debug)

        self.__logger = Logger(logger_name="rubix-cli")
        self.__logger.init(debug=debug)

    @contextmanager
    def __tty_session(self):
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

        cmd = textwrap.dedent(cmd)
        raw_response, raw_error = serial_session.send_command(data=cmd)

        response = self.__parse_command_response(raw_response)
        errors = self.__parse_command_response(raw_error)

        return response, errors

    def __handle_command_response(self, response: str, errors: str | None):
        if errors:
            self.__logger.exception(errors)
            return

        self.__logger.info(response)

    def ls(self, path: str = "/"):
        self.__logger.info(f"ls at '{path}'")

        with self.__tty_session() as session:
            cmd = f"""
                import uos

                for file in uos.listdir('{path}'):
                    path = '{path}' + '/' + file
                    stats = uos.stat(path)

                    st_size = str(stats[6])
                    st_ctime = str(stats[9])

                    row = st_size + " " + st_ctime + " " + path

                    print(row)
            """

            data, errors = self.__send_command(cmd, session)

            if errors:
                self.__logger.exception(errors)
                return

            self.__logger.info(data)

    def rmdir(self, path: str):
        self.__logger.info(f"rmdir '{path}'")

        with self.__tty_session() as session:
            cmd = f"""
                import uos

                def file_exists(path):
                    try:
                        uos.stat(path)

                        return True
                    except OSError:
                        return False

                def rmdir(path):
                    uos.chdir(path)

                    for file in uos.listdir():
                        try:
                            uos.remove(file)
                        except OSError:
                            pass
                            
                    for dir in uos.listdir():
                        rmdir(dir)

                    uos.chdir("..")
                    os.rmdir("{path}")

                if not file_exists("{path}"):
                    print("{path} doesn't exist")
                else:
                    rmdir("{path}")
            """

            data, errors = self.__send_command(cmd, session)

            if errors:
                self.__logger.exception(errors)
                return

            self.__logger.info(data)
