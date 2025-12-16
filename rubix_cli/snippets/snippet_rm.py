from rubix_cli.snippets import SnippetBase


class SnippetRm(SnippetBase):
    def get_code(self, kwargs):
        return self._load_snippet("rm", **kwargs)
