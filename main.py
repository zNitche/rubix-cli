import os
import termios


def main():
    interface = "/dev/tty.usbmodem12401"
    baudrate = 115200

    tty_fd = os.open(interface, os.O_RDWR | os.O_NONBLOCK)

    try:
        ori_tty_attr = termios.tcgetattr(tty_fd)
        iflag, oflag, cflag, lflag, ispeed, ospeed, cc = ori_tty_attr

        print(f"orig_tty_attr = {ori_tty_attr}")

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

        runtime_tty_attr = termios.tcgetattr(tty_fd)
        print(f"runtime_tty_attr = {runtime_tty_attr}")

        print(os.read(tty_fd, 100))

        # turn on onboard led
        os.write(tty_fd, b"import machine\r\n")
        os.write(tty_fd, b"led = machine.Pin('LED', machine.Pin.OUT)\r\n")
        os.write(tty_fd, b"led.on()\r\n")

        print(os.read(tty_fd, 200))

    except Exception as e:
        print(e)

    os.close(tty_fd)


if __name__ == "__main__":
    main()
