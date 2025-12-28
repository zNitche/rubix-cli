class MP_CONSTS:
    # hex
    EOT_HEX = b"\x04"
    ETX_HEX = b"\x03"
    STX_HEX = b"\x02"
    SOH_HEX = b"\x01"

    RAW_PASTE_MODE_HEX = b"\x05A\x01"
    SUCCESS_RESPONSE_END_HEX = b"\x01"

    # text
    SOFT_REBOOT = b"soft reboot\r\n"


class TERM_COLORS:
    BLACK = '\033[90m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'

    END = '\033[0m'
