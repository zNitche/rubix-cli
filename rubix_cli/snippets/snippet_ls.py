from rubix_cli.snippets import SnippetBase


class SnippetLs(SnippetBase):
    def get_code(self, kwargs):
        return self._load_snippet("ls", **kwargs)
