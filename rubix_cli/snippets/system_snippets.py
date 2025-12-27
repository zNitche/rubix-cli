from datetime import datetime
from rubix_cli.snippets import SnippetBase


class SnippetUname(SnippetBase):
    def __init__(self):
        super().__init__()

        self.snippet_name = "uname"


class SnippetGetRtc(SnippetBase):
    def __init__(self):
        super().__init__()

        self.snippet_name = "get_rtc"


class SnippetSetRtc(SnippetBase):
    def __init__(self):
        super().__init__()

        self.snippet_name = "set_rtc"

    def get_code(self, args=None):
        now = datetime.now()

        args = {
            "year": now.year,
            "month": now.month,
            "day": now.day,
            "weekday": now.weekday(),
            "hours": now.hour,
            "minutes": now.minute,
            "seconds": now.second,
            "subseconds": now.microsecond
        }

        return self._load_snippet(self.snippet_name, args)  # type: ignore
