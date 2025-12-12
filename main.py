import textwrap
from rubix_cli.core import SerialTTY

def main():
    interface = "/dev/tty.usbmodem112401"

    serial = SerialTTY(interface=interface)

    try:
        serial.soft_reboot()
        serial.enter_raw_repl()

        cmd = """
            import machine
            
            led = machine.Pin('LED', machine.Pin.OUT)

            led.toggle()
        """

        cmd = textwrap.dedent(cmd)

        cmd_response = serial.send_command(cmd)
        print(f"cmd resp = {cmd_response}")

        serial.exit_raw_repl()

    except Exception as e:
        print(e)

    serial.close()


if __name__ == "__main__":
    main()
