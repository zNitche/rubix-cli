import os
import termios
import select
import time
from rubix_cli.core.utils import Logger
from rubix_cli.core.consts import MP_CONSTS


class SerialTTY:
    def __init__(self, interface: str, baudrate: int = 115200, timeout: int = 2,
                 write_buffer_size: int = 128, debug: bool = False):

        self.__interface = interface

        self.__baudrate = baudrate
        self.__timeout = timeout
        self.__write_buffer_size = write_buffer_size

        self.__logger = self.__get_logger(debug)

        self.__tty_fd = self.__open_fd()
        self.__setup_interface()

    def __get_logger(self, debug: bool):
        logger = Logger(logger_name="rubix-cli-serial")
        logger.init(debug=debug)

        return logger

    def __open_fd(self):
        return os.open(self.__interface, os.O_RDWR | os.O_NONBLOCK)

    def close(self):
        os.close(self.__tty_fd)

    def __setup_interface(self):
        ori_tty_attr = termios.tcgetattr(self.__tty_fd)
        iflag, oflag, cflag, lflag, ispeed, ospeed, cc = ori_tty_attr

        ispeed = self.__baudrate
        ospeed = self.__baudrate

        cc[termios.VTIME] = int(self.__timeout * 10)
        cc[termios.VMIN] = 0

        # enables raw mode
        cflag |= (termios.CLOCAL | termios.CREAD)

        termios.tcsetattr(
            self.__tty_fd,
            termios.TCSANOW,
            [iflag, oflag, cflag, lflag, ispeed, ospeed, cc])

    def __interrupt_current_run(self):
        for _ in range(2):
            self.write(MP_CONSTS.ETX_HEX)
            time.sleep(0.01)

    def write(self, data: str | bytes):
        data = data if isinstance(
            data, (bytes)) else data.encode()  # type: ignore

        os.write(self.__tty_fd, data)

    def read(self, bytes_to_read: int):
        ready = select.select([self.__tty_fd], [], [], self.__timeout)

        if ready[0]:
            return os.read(self.__tty_fd, bytes_to_read)

        else:
            return None

    def read_until(self, stop_at: bytes):
        self.__logger.debug(f"reading untill {stop_at} ...")
        buff = b""

        while True:
            read_data = self.read(1)

            if read_data is None:
                break

            buff += read_data

            if stop_at and buff.endswith(stop_at):
                break
        
        self.__logger.debug(message=f"buff: {buff}")

        return buff

    def send_command(self, data: bytes | str):
        data_length = len(data)

        for chunk_start in range(0, data_length, self.__write_buffer_size):
            chunk_offset = min(
                chunk_start + self.__write_buffer_size, data_length)
            chunk = data[chunk_start:chunk_offset]

            self.write(chunk)
            time.sleep(0.01)

        self.write(MP_CONSTS.EOT_HEX)

        is_success = self.read_until(stop_at=MP_CONSTS.EOT_HEX)

        if is_success is None:
            raise Exception("response is None")

        if is_success.endswith(MP_CONSTS.EOT_HEX):
            self.__logger.debug(
                f"successfully wrote {len(data)} bytes to device")

        response = self.read_until(stop_at=MP_CONSTS.EOT_HEX)
        errors = self.read_until(stop_at=MP_CONSTS.EOT_HEX)

        return response, errors

    def soft_reboot(self):
        self.__interrupt_current_run()

        self.write(MP_CONSTS.EOT_HEX)
        time.sleep(0.1)

        soft_reboot_state = self.read_until(stop_at=MP_CONSTS.SOFT_REBOOT)

        if not soft_reboot_state.endswith(MP_CONSTS.SOFT_REBOOT):
            raise Exception("soft restart failed")

        self.__logger.debug("rebooted")

    def enter_raw_repl(self):
        self.__interrupt_current_run()

        # enter raw repl
        self.write(MP_CONSTS.SOH_HEX)
        time.sleep(0.1)

        # enter raw-paste mode
        self.write(MP_CONSTS.RAW_PASTE_MODE_HEX)
        self.read_until(b">R")

        write_response = self.read(4)

        if not write_response or not write_response.endswith(MP_CONSTS.SUCCESS_RESPONSE_END_HEX):
            raise Exception("failed to enter raw REPL")

        self.__logger.debug("entered raw repl")

    def exit_raw_repl(self):
        self.write(b"\r\x02")

        self.__logger.debug("exit from raw repl")
