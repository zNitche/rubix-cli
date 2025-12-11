import os
import termios
import select
import time


def read_from_tty(file_descriptor: int, length: int | None = None,
                  stop_at: bytes | None = None,
                  timeout: int = 2):
    buff = b""
    bytes_to_read = 1 if not length else length

    while True:
        ready = select.select([file_descriptor], [], [], timeout)

        if ready[0]:
            buff += os.read(file_descriptor, bytes_to_read)

        else:
            break

        if stop_at and buff.endswith(stop_at):
            break

        if length and len(buff) == length:
            break

    return buff


# https://docs.micropython.org/en/latest/reference/repl.html#raw-mode-and-raw-paste-mode
def enter_raw_repl(file_descriptor: int):
    etx_hex = b"\x03"

    os.write(file_descriptor, etx_hex)
    time.sleep(0.5)
    os.write(file_descriptor, etx_hex)
    time.sleep(0.5)

    # enter raw repl
    os.write(file_descriptor, b"\x01")

    # enter raw-paste mode
    os.write(file_descriptor, b"\x05A\x01")
    read_from_tty(file_descriptor, stop_at=b">R")

    flow_control_window_size = read_from_tty(file_descriptor, length=2)
    print(f"flow_control_window_size={int.from_bytes(flow_control_window_size)}")

    success_response = read_from_tty(file_descriptor, length=2)

    if not success_response.endswith(b"\x00\x01"):
        raise Exception("failed to enter raw REPL")

    print("entered raw repl")


def exit_raw_repl(file_descriptor: int):
    os.write(file_descriptor, b'\r\x02')


def soft_reboot(file_descriptor: int):
    ctrl_d_hex = b"\x04"

    os.write(file_descriptor, ctrl_d_hex)
    soft_reboot_state = read_from_tty(
        file_descriptor, stop_at=b'soft reboot\r\n')

    if not soft_reboot_state.endswith(b'soft reboot\r\n'):
        raise Exception("soft restart failed")

    print("rebooted")


def write_bytes_to_tty(file_descriptor: int, data: bytes):
    os.write(file_descriptor, data)
    time.sleep(0.01)

    os.write(file_descriptor, b"\x04")

    is_success = read_from_tty(file_descriptor, stop_at=b"\x04")

    if is_success.endswith(b"\x04"):
        print(f"successfully wrote {len(data)} bytes to device")

    response = read_from_tty(file_descriptor, stop_at=b"\x04")

    print(f"response = {response}")


def main():
    interface = "/dev/tty.usbmodem12301"
    baudrate = 115200

    tty_fd = os.open(interface, os.O_RDWR | os.O_NONBLOCK)

    try:
        ori_tty_attr = termios.tcgetattr(tty_fd)
        iflag, oflag, cflag, lflag, ispeed, ospeed, cc = ori_tty_attr

        # print(f"orig_tty_attr = {ori_tty_attr}")

        ispeed = baudrate
        ospeed = baudrate

        timeout = 5

        cc[termios.VTIME] = int(timeout * 10)
        # min number of characters for read
        cc[termios.VMIN] = 0

        # enables raw mode
        cflag |= (termios.CLOCAL | termios.CREAD)

        termios.tcsetattr(
            tty_fd,
            termios.TCSANOW,
            [iflag, oflag, cflag, lflag, ispeed, ospeed, cc])

        # runtime_tty_attr = termios.tcgetattr(tty_fd)
        # print(f"runtime_tty_attr = {runtime_tty_attr}")

        # turn on onboard led
        # os.write(tty_fd, b"import machine\r\n")
        # os.write(tty_fd, b"led = machine.Pin('LED', machine.Pin.OUT)\r\n")
        # os.write(tty_fd, b"led.on()\r\n")

        # os.write(tty_fd, b"print('hello pico')\r\n")

        soft_reboot(file_descriptor=tty_fd)

        # os.write(tty_fd, b"\x01\x05A\x01print(123)\x04")
        # print(read_from_tty(file_descriptor=tty_fd))

        enter_raw_repl(tty_fd)

        write_bytes_to_tty(tty_fd, b'print("hello pico")')

        exit_raw_repl(tty_fd)

    except Exception as e:
        print(e)

    os.close(tty_fd)


if __name__ == "__main__":
    main()
