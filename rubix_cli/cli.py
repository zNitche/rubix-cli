import argparse
from rubix_cli import __version__
from rubix_cli import commands as cli_commands
from rubix_cli.core import Commander
from rubix_cli.core.cli import CliCommandBase
from rubix_cli.core.consts import TERM_COLORS
from rubix_cli.core import common_utils


class CLI:
    def __init__(self, commander: Commander):
        self.__commander = commander
        self.__commands = self.__get_commands()

    def __get_commands(self):
        commands: list[CliCommandBase] = []

        commands.append(cli_commands.CliLsCommand(self.__commander))

        return commands

    def list_commands(self):
        for cmd in self.__commands:
            common_utils.print_color(f"### {cmd.cli_invoker}", TERM_COLORS.GREEN)

            args = cmd.args
            args_count = len(args.keys()) if args else 0

            if args and args_count > 0:
                for arg_name in args:
                    common_utils.print_color(
                        f"\t{arg_name}: {args[arg_name]}", TERM_COLORS.MAGENTA)

            if cmd.description:
                print(f"description: {cmd.description}")

            print("\n")

    def execute_command(self, command: str, *args):
        cmd = None

        for c in self.__commands:
            if c.cli_invoker == command:
                cmd = c
                break

        if not cmd:
            raise Exception(f"unknown command '{command}'")

        cmd.command.exec(*args)


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
