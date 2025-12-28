import argparse
import inspect
from rubix_cli import __version__
from rubix_cli.core import Commander
from rubix_cli.core.consts import TERM_COLORS
from rubix_cli.core import common_utils


class CLI:
    def __init__(self, commander: Commander):
        self.__commander = commander

        self.__commands = self.__get_commands()

    def __get_func_args(self, func):
        args = {}
        inspect_data = inspect.signature(func).parameters

        for key, val in inspect_data.items():
            args[key] = val.annotation.__name__

        return None if len(args.keys()) == 0 else args

    def __get_commands(self):
        commands = {
            "l_repl": {
                "description": "",
                "func": self.__commander.listen_on_repl,
            },
            "reboot": {
                "description": "",
                "func": self.__commander.soft_reboot,
            },
            "ls": {
                "description": "",
                "func": self.__commander.ls,
            },
            "rm": {
                "description": "",
                "func": self.__commander.rm,
            },
            "rmdir": {
                "description": "",
                "func": self.__commander.rmdir,
            },
            "mkdir": {
                "description": "",
                "func": self.__commander.mkdir,
            },
            "purge": {
                "description": "",
                "func": self.__commander.purge,
            },
            "set_rtc": {
                "description": "",
                "func": self.__commander.set_rtc,
            },
            "get_rtc": {
                "description": "",
                "func": self.__commander.get_rtc,
            },
            "uname": {
                "description": "",
                "func": self.__commander.uname,
            },
            "upload_file": {
                "description": "",
                "func": self.__commander.upload_file,
            },
            "get_file": {
                "description": "",
                "func": self.__commander.get_file,
            },
            "flash": {
                "description": "",
                "func": self.__commander.flash,
            }
        }

        for cmd in commands:
            cmd_data = commands[cmd]
            cmd_data["args"] = self.__get_func_args(cmd_data["func"])

        return commands

    def list_commands(self):
        for command_name in self.__commands:
            cmd_details = self.__commands[command_name]

            common_utils.print_color(f"### {command_name}", TERM_COLORS.GREEN)

            args = cmd_details['args']
            args_count = len(args.keys()) if args else 0

            if args_count > 0:
                for arg_name in args:
                    common_utils.print_color(
                        f"\t{arg_name}: {args[arg_name]}", TERM_COLORS.MAGENTA)

            description = cmd_details.get("description")

            if description:
                print(f"description: {description}")

            print("\n")

    def execute_command(self, command: str, *args):
        command_data = self.__commands.get(command)

        if not command_data:
            raise Exception(f"unknown command '{command}'")

        command_data["func"](*args)


def main(args: argparse.Namespace):
    show_version = args.version
    debug = args.debug

    interface = args.device

    timeout = args.timeout
    baudrate = args.baudrate
    write_buffer_size = args.write_buffer_size

    cmd = args.cmd
    cmd_args = args.cmd_args

    show_commands = args.commands

    commander = Commander(interface=interface, debug=debug, timeout=timeout,
                          baudrate=baudrate, write_buffer_size=write_buffer_size)
    cli = CLI(commander=commander)

    if show_version:
        print(f"v{__version__}")
        return

    if show_commands:
        cli.list_commands()
        return

    if not cmd:
        raise Exception("cmd not passed")

    cli.execute_command(cmd, *cmd_args)


def get_args():
    argument_parser = argparse.ArgumentParser()

    argument_parser.add_argument("--version", action=argparse.BooleanOptionalAction,
                                 default=False, required=False)

    argument_parser.add_argument(
        "--device", type=str, help="example, /dev/tty1", required=False)

    argument_parser.add_argument(
        "--timeout", type=float, default=1.0, required=False)

    argument_parser.add_argument(
        "--baudrate", type=int, default=115200, required=False)

    argument_parser.add_argument(
        "--write-buffer-size", type=int, default=128, required=False)

    argument_parser.add_argument(
        '--cmd', help='command name, for example ls /', required=False)

    argument_parser.add_argument(
        'cmd_args', nargs='*', help='command args, for example /')

    argument_parser.add_argument("--commands", action=argparse.BooleanOptionalAction,
                                 default=False, help="get available commands", required=False)

    argument_parser.add_argument("--debug", action=argparse.BooleanOptionalAction,
                                 default=False, help="debug mode", required=False)

    return argument_parser.parse_args()


def run():
    args = get_args()

    main(args)
