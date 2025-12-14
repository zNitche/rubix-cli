import argparse
import inspect
from rubix_cli.core import Commander


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
            }
        }

        for cmd in commands:
            cmd_data = commands[cmd]
            cmd_data["args"] = self.__get_func_args(cmd_data["func"])

        return commands

    def list_commands(self):
        for command_name in self.__commands:
            cmd_details = self.__commands[command_name]

            print(f"### {command_name}")
            print(f"args: {cmd_details['args']}")

            description = cmd_details.get("description")

            if description:
                print(f"description: {description}")

    def execute_command(self, command: str, *args):
        command_data = self.__commands.get(command)

        if not command_data:
            raise Exception(f"unknown command '{command}'")

        command_data["func"](*args)


def main(args: argparse.Namespace):
    interface = args.device

    cmd = args.cmd
    cmd_args = args.cmd_args

    show_commands = args.commands
    debug = args.debug

    commander = Commander(interface=interface, debug=debug)
    cli = CLI(commander=commander)

    if show_commands:
        cli.list_commands()
        return

    if not cmd:
        raise Exception("cmd not passed")

    cli.execute_command(cmd, *cmd_args)


def get_args():
    argument_parser = argparse.ArgumentParser()

    argument_parser.add_argument(
        "--device", type=str, help="example, /dev/tty1", required=True)

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
