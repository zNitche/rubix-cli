from rubix_cli.snippets import SnippetBase


class SnippetCatFile(SnippetBase):
    def __init__(self):
        super().__init__()

        self.snippet_name = "cat_file"


class SnippetLs(SnippetBase):
    def __init__(self):
        super().__init__()

        self.snippet_name = "ls"


class SnippetMkDir(SnippetBase):
    def __init__(self):
        super().__init__()

        self.snippet_name = "mkdir"


class SnippetPurge(SnippetBase):
    def __init__(self):
        super().__init__()

        self.snippet_name = "purge"


class SnippetRm(SnippetBase):
    def __init__(self):
        super().__init__()

        self.snippet_name = "rm"


class SnippetRmDir(SnippetBase):
    def __init__(self):
        super().__init__()

        self.snippet_name = "rmdir"


class SnippetUploadFile(SnippetBase):
    def __init__(self):
        super().__init__()

        self.snippet_name = "upload_file"
