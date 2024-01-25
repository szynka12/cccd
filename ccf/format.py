import textwrap as tw


def default_format_head(
    name: str,
    formatted_description: str,
    n_lines_data: int | None = None,
    write_lines: bool = False,
    comment_text: str = "#",
) -> str:
    meta_data = (
        (
            "{} - The header contains {} lines\n".format(
                comment_text,
                n_lines_data + 7 + formatted_description.count("\n"),
            )
            + f"{comment_text}\n"
        )
        if write_lines and n_lines_data is not None
        else ""
    )

    return (
        f"{comment_text} {name}:\n"
        + f"{comment_text}\n"
        + meta_data
        + f"{formatted_description}{comment_text}\n"
        + f"{comment_text} Data entries are described below:\n"
        + f"{comment_text}\n"
    )


def default_format_description(
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


def default_format_entry(
    name: str, formatted_description: str, comment_text: str = "#"
) -> str:
    # return "# " + self.name_ + ":\n" + desc_wrapped + "\n#\n"
    return f"{comment_text} {name}:\n{formatted_description}{comment_text}\n"
