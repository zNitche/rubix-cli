from rubix_cli.snippets import SnippetBase


class SnippetPurge(SnippetBase):
    def get_code(self, kwargs):
        return self._load_snippet("purge", **kwargs)
