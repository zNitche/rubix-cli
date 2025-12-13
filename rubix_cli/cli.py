import argparse
import inspect
from rubix_cli.core import Commander


def __get_func_args(func):
    args = {}
    inspect_data = inspect.signature(func).parameters

    for key, val in inspect_data.items():
        args[key] = val.annotation.__name__

    return args


def get_commands(commander: Commander):
    commands = {
        "ls": {
            "description": "",
            "func": commander.list_files,
            "args": __get_func_args(commander.list_files)
        }
    }

    return commands


def list_commands(commander: Commander):
    commands = get_commands(commander)

    for command_name in commands:
        cmd_details = commands[command_name]

        print(f"### {command_name}")
        print(f"args: {cmd_details['args']}")

        description = cmd_details.get("description")

        if description:
            print(f"description: {description}")


def main(args: argparse.Namespace):
    interface = args.interface
    debug = args.debug

    commander = Commander(interface=interface, debug=debug)

    list_commands(commander)

    files = commander.list_files(path="/")

    print(files)


def get_args():
    argument_parser = argparse.ArgumentParser()

    argument_parser.add_argument(
        "--interface", type=str, help="example, /dev/tty1", required=True)

    argument_parser.add_argument("--debug", action=argparse.BooleanOptionalAction,
                                 default=False, help="debug mode", required=False)

    return argument_parser.parse_args()


def run():
    args = get_args()

    main(args)
