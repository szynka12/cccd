import polars as pl
from DataDescription import DataDescription, format_description
from typing import List, Callable, Dict, Any


def default_data_descriptor(name: str, desc: str) -> DataDescription:
    return DataDescription(name, desc)


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


class DataSet(DataDescription):
    def __init__(
        self,
        name: str,
        description: str,
        desc_formatter: Callable[[str], str] = format_description,
        entry_formatter: Callable[[str, str], str] = default_format_head,
        data_descriptor: Callable[
            [str, str], DataDescription
        ] = default_data_descriptor,
    ):
        DataDescription.__init__(
            self, name, description, desc_formatter, entry_formatter
        )

        self.data_descriptor_ = data_descriptor
        self.data_descriptions_: List[DataDescription] = []
        self.data_: pl.DataFrame = pl.DataFrame()

    def __str__(self):
        return self.to_text()

    def generate_header(
        self,
        header_entry_opts: Dict[str, Any] = {},
        header_desc_opts: Dict[str, Any] = {},
        entry_opts: Dict[str, Any] = {},
        desc_opts: Dict[str, Any] = {},
    ) -> str:

        data_entries_text = "".join(
            [x.to_text(entry_opts, desc_opts) for x in self.data_descriptions_]
        )
        if (
            "write_lines" in header_entry_opts
            and header_entry_opts["write_lines"] is True
        ):
            n_lines = data_entries_text.count("\n")
            header_entry_opts["n_lines_data"] = n_lines

        return (
            super().to_text(header_entry_opts, header_desc_opts)
            + data_entries_text
        )

    def append_data_raw(
        self, description: DataDescription, data: pl.DataFrame
    ):
        self.data_descriptions_.append(description)
        self.data_ = pl.concat(
            [self.data_, data],
            how="horizontal",
        )

    def append(self, name: str, desc: str, value: Any):
        d = self.data_descriptor_(name, desc)
        self.append_data_raw(d, pl.DataFrame({d.column_name(): value}))


def write_ds(
    ds: DataSet,
    file_name: str,
    header_entry_opts: Dict[str, Any] = {},
    header_desc_opts: Dict[str, Any] = {},
    entry_opts: Dict[str, Any] = {},
    desc_opts: Dict[str, Any] = {},
):

    with open(file_name, mode="w") as file:
        file.write(
            ds.generate_header(
                header_entry_opts, header_desc_opts, entry_opts, desc_opts
            )
        )

    with open(file_name, mode="ab") as file:
        ds.data_.write_csv(file)
