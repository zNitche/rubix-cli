from rubix_cli.core.snippets import SnippetBase


class SnippetLS(SnippetBase):
    def __init__(self):
        super().__init__()

    def get_code(self, kwargs):
        return self._load_snippet("list_files", **kwargs)
