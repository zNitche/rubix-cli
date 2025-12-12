import os
import termios
import select
import time
from rubix_cli.core.utils import Logger
from rubix_cli.core import MP_CONSTS


class SerialTTY:
    def __init__(self, interface: str, baudrate: int = 115200, timeout: int = 2):
        self.__interface = interface
        self.__baudrate = baudrate
        self.__timeout = timeout

        self.__logger = self.__get_logger()

        self.__tty_fd = self.__open_fd()
        self.__setup_interface()

    def __get_logger(self):
        l = Logger(logger_name="rubix-cli")
        l.init()

        return l

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
        buff = b""

        while True:
            read_data = self.read(1)

            if read_data is None:
                break

            buff += read_data

            if stop_at and buff.endswith(stop_at):
                break

        return buff

    def send_command(self, data: bytes | str):
        self.write(data=data)
        time.sleep(0.05)

        self.write(MP_CONSTS.EOT_HEX)

        is_success = self.read_until(stop_at=MP_CONSTS.EOT_HEX)

        if is_success.endswith(MP_CONSTS.EOT_HEX):
            self.__logger.info(
                f"successfully wrote {len(data)} bytes to device")

        return self.read_until(stop_at=MP_CONSTS.EOT_HEX)

    def soft_reboot(self):
        self.write(MP_CONSTS.EOT_HEX)
        time.sleep(0.1)

        soft_reboot_state = self.read_until(stop_at=MP_CONSTS.SOFT_REBOOT)

        if not soft_reboot_state.endswith(MP_CONSTS.SOFT_REBOOT):
            raise Exception("soft restart failed")

        self.__logger.info("rebooted")

    def enter_raw_repl(self):
        for _ in range(2):
            self.write(MP_CONSTS.ETX_HEX)
            time.sleep(0.5)

        # enter raw repl
        self.write(MP_CONSTS.SOH_HEX)

        # enter raw-paste mode
        self.write(MP_CONSTS.RAW_PASTE_MODE_HEX)
        self.read_until(b">R")

        flow_control_window_size = self.read(2)

        if not flow_control_window_size:
            raise Exception("can't read flow control window size")

        flow_control_window_size = int.from_bytes(
            flow_control_window_size, byteorder="little")

        success_response = self.read(2)

        if not success_response or not success_response.endswith(MP_CONSTS.SUCCESS_RESPONSE_END_HEX):
            raise Exception("failed to enter raw REPL")

        self.__logger.info("entered raw repl")

    def exit_raw_repl(self):
        self.write(b"\r\x02")

        self.__logger.info("exit from raw repl")
