from rubix_cli.snippets import SnippetBase


class SnippetMkDir(SnippetBase):
    def __init__(self):
        super().__init__()

    def get_code(self, kwargs):
        return self._load_snippet("mkdir", **kwargs)
