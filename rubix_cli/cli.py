import argparse
from rubix_cli.core import Commander


def main(args: argparse.Namespace):
    interface = args.interface
    debug = args.debug

    commander = Commander(interface=interface, debug=debug)
    files = commander.list_files()

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
