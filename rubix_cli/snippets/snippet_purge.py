from rubix_cli.snippets import SnippetBase


class SnippetPurge(SnippetBase):
    def __init__(self):
        super().__init__()

        self.snippet_name = "purge"
