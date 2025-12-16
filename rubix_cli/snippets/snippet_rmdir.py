from rubix_cli.snippets import SnippetBase


class SnippetRmDir(SnippetBase):
    def get_code(self, kwargs):
        return self._load_snippet("rmdir", **kwargs)
