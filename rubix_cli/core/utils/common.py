from rubix_cli.core.consts import TERM_COLORS


def print_color(msg: str, color: str):
    print(f"{color}{msg}{TERM_COLORS.END}")
