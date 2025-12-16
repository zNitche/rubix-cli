from rubix_cli.snippets import SnippetBase


class SnippetUname(SnippetBase):
    def __init__(self):
        super().__init__()

        self.snippet_name = "uname"
