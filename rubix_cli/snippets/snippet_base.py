import os
import textwrap
import re


class SnippetBase:
    def __init__(self):
        self.__root_path = os.path.dirname(os.path.abspath(__file__))
        self.__snippets_path = os.path.join(self.__root_path, "templates")

    def __inject_sub_snippet(self, snippet: str):
        subs_path = os.path.join(self.__snippets_path, "common")

        subs = re.findall(r"<mod>(.*)</mod>", snippet)

        for sub_name in subs:
            tag = f"<mod>{sub_name}</mod>"
            sub_snippet_path = os.path.join(subs_path, f"{sub_name}.py.snippet")

            if not os.path.exists(sub_snippet_path):
                raise Exception(f"sub snippet '{sub_name}' doesn't exist")
            
            with open(sub_snippet_path, "r") as file:
                sub_content = file.read()

            snippet = snippet.replace(tag, sub_content)

        return snippet

    def _load_snippet(self, name: str, **kwargs):
        file_path = os.path.join(self.__snippets_path, f"{name}.py.snippet")

        if not os.path.exists(file_path):
            raise Exception(f"snippet '{name}' doesn't exist")

        with open(file_path, "r") as file:
            snippet_content = file.read()

        snippet_content = self.__inject_sub_snippet(snippet_content)
        snippet_content = snippet_content.format(**kwargs)

        return textwrap.dedent(snippet_content)

    def get_code(self, kwargs):
        raise NotImplementedError()
