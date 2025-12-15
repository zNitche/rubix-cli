import os
import textwrap
import re


class SnippetBase:
    def __init__(self):
        self.__root_path = os.path.dirname(os.path.abspath(__file__))
        self.__snippets_path = os.path.join(self.__root_path, "templates")

    def __find_tags(self, snippet: str, tag_name: str):
        tags_in_snippet = re.findall(
            rf"<{tag_name}>(.*)</{tag_name}>", snippet)
        tags = []

        for tag_value in tags_in_snippet:
            item = {
                "tag_name": tag_name,
                "value": tag_value,
                "tag": f"<{tag_name}>{tag_value}</{tag_name}>"
            }

            tags.append(item)

        return tags

    def __inject_sub_snippet(self, snippet: str):
        subs_path = os.path.join(self.__snippets_path, "common")

        subs_tags = self.__find_tags(snippet, "mod")

        for tag in subs_tags:
            sub_name = tag['value']
            sub_snippet_path = os.path.join(
                subs_path, f"{sub_name}.py-snippet")

            if not os.path.exists(sub_snippet_path):
                raise Exception(f"sub snippet '{sub_name}' doesn't exist")

            with open(sub_snippet_path, "r") as file:
                sub_content = file.read()

            snippet = snippet.replace(tag['tag'], sub_content)

        return snippet
    
    def __remove_comments(self, snippet: str):
        subs_tags = self.__find_tags(snippet, "com")

        for tag in subs_tags:
            snippet = snippet.replace(tag['tag'], "")

        return snippet
    
    def __inject_variables(self, snippet: str, variables: dict[str, str]):
        subs_tags = self.__find_tags(snippet, "var")

        for tag in subs_tags:
            variable_name = tag['value']
            var = variables.get(variable_name)

            if var is None:
                raise Exception(f"failed to inject '{variable_name}' into snippet")

            snippet = snippet.replace(tag['tag'], var)

        return snippet

    def _load_snippet(self, name: str, **kwargs):
        file_path = os.path.join(self.__snippets_path, f"{name}.py-snippet")

        if not os.path.exists(file_path):
            raise Exception(f"snippet '{name}' doesn't exist")

        with open(file_path, "r") as file:
            snippet_content = file.read()

        snippet_content = self.__inject_sub_snippet(snippet_content)
        snippet_content = self.__remove_comments(snippet_content)

        snippet_content = self.__inject_variables(snippet_content, variables=kwargs)

        return textwrap.dedent(snippet_content)

    def get_code(self, kwargs):
        raise NotImplementedError()
