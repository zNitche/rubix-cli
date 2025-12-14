import os
import textwrap


class SnippetBase:
    def __init__(self):
        self.__root_path = os.path.dirname(os.path.abspath(__file__))

    def _load_snippet(self, name: str, **kwargs):
        file_path = os.path.join(self.__root_path, "templates", f"{name}.py.snippet")

        if not os.path.exists(file_path):
            raise Exception(f"{file_path} doesn't exist")

        with open(file_path, "r") as file:
            snippet_content = file.read()

        snippet_content = snippet_content.format(**kwargs)

        return textwrap.dedent(snippet_content)

    def get_code(self, kwargs):
        raise NotImplementedError()
