from contextlib import contextmanager
import textwrap
from rubix_cli.core import SerialTTY, MP_CONSTS
from rubix_cli.core.utils import Logger


class Commander:
    def __init__(self, interface: str):
        self.__serial = SerialTTY(interface=interface)

        self.__logger = Logger(logger_name="rubix-cli")
        self.__logger.init()

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
            ("\r\n", "")
        ]

        for it in subs_to_replace:
            decoded_response = decoded_response.replace(it[0], it[1])

        return decoded_response

    def __send_command(self, cmd: str, serial_session: SerialTTY):
        cmd = textwrap.dedent(cmd)
        r = serial_session.send_command(data=cmd)

        response = self.__parse_command_response(r[0])
        errors = self.__parse_command_response(r[1])

        return response, errors

    def list_files(self, path: str = "/"):
        with self.__tty_session() as session:
            cmd = f"""
                import uos
                
                files = uos.listdir('{path}')
                print(','.join(files))
            """

            response = self.__send_command(cmd, session)
            data = response[0]
            errors = response[1]

            if errors:
                raise Exception(errors)

            return data.split(',')
