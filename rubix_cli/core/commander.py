import time
from rubix_cli.core import SerialTTY
from rubix_cli.core.consts import MP_CONSTS
from rubix_cli.core.utils import Logger


class Commander:
    def __init__(self, interface: str | None, debug: bool = False,
                 timeout: float = 1.0, baudrate: int = 115200,
                 write_buffer_size: int = 128):

        self.__serial = self.__setup_serial_tty(interface, debug, timeout,
                                                baudrate, write_buffer_size)

        self._logger = Logger(logger_name="rubix-cli")
        self._logger.init(debug=debug)

    def __setup_serial_tty(self, interface: str | None, debug: bool, timeout: float,
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

    def send_command(self, cmd: str, reboot: bool = True):
        self._logger.debug(f"sending: {cmd}")

        if self.__serial is None:
            raise Exception("interface has not been specified")

        raw_response = b""
        raw_error = b""

        if reboot:
            self._logger.debug(message="soft reboot")
            self.__serial.soft_reboot()

        self.__serial.enter_raw_repl()

        try:
            raw_response, raw_error = self.__serial.send_command(data=cmd)

        except Exception as e:
            self._logger.exception("error while processing tty session")
            raise e

        self.__serial.exit_repl()

        response = self.__parse_command_response(raw_response)
        errors = self.__parse_command_response(raw_error)

        return response, errors

    def handle_command_response(self, response: str, errors: str | None, raise_exception_on_errors: bool = False):
        if errors:
            self._logger.exception(errors)

            if raise_exception_on_errors:
                raise Exception("command returned some errors")

            return

        if response:
            self._logger.info(response)

    def default_cmd_handler(self, cmd: str, reboot: bool = True, raise_exception_on_errors: bool = False):
        data, errors = self.send_command(cmd, reboot=reboot)
        self.handle_command_response(data, errors, raise_exception_on_errors)

    def listen_on_repl(self):
        if self.__serial is None:
            raise Exception("interface has not been specified")

        try:
            self.soft_reboot()
            self.__serial.enter_repl()

            time.sleep(0.1)
            self.soft_reboot()

            while True:
                read_data = self.__serial.read(128, timeout=None)

                if read_data is None:
                    break

                print(read_data.decode(), end="")

        except KeyboardInterrupt:
            self.__serial.exit_repl()
            self._logger.info("exiting repl")

    def soft_reboot(self):
        if self.__serial is None:
            raise Exception("interface has not been specified")

        self.__serial.soft_reboot()
