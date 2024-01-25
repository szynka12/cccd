import textwrap as tw
from typing import Callable, Optional, Dict, Any


def format_description(
    description_text: str,
    width: int = 80,
    indent_text: str = "    ",
    comment_text="#",
    break_long_words: bool = False,
    tabsize: int = 4,
) -> str:
    return "{}\n".format(
        tw.fill(
            tw.dedent(description_text),
            width=width,
            initial_indent=f"{comment_text}{indent_text}",
            subsequent_indent=f"{comment_text}{indent_text}",
            break_long_words=break_long_words,
            tabsize=tabsize,
            expand_tabs=True,
        )
    )


def format_entry(
    name: str, formatted_description: str, comment_text: str = "#"
) -> str:
    # return "# " + self.name_ + ":\n" + desc_wrapped + "\n#\n"
    return f"{comment_text} {name}:\n{formatted_description}{comment_text}\n"


class DataDescription:
    def __init__(
        self,
        name: str,
        description: str,
        desc_formatter: Callable[[str], str] = format_description,
        entry_formatter: Callable[[str, str], str] = format_entry,
    ):
        self.name_: str = name
        self.description_: str = description
        self.desc_formatter_: Callable[[str], str] = desc_formatter
        self.entry_formatter_: Callable[[str, str], str] = entry_formatter

    def __str__(self) -> str:
        return self.to_text()

    def to_text(
        self, entry_opts: Dict[str, Any] = {}, desc_opts: Dict[str, Any] = {}
    ) -> str:
        formatted_description = self.desc_formatter_(
            self.description_, **desc_opts
        )
        return self.entry_formatter_(
            self.name_, formatted_description, **entry_opts
        )

    def column_name(self) -> str:
        return self.name_
