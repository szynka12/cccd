import polars as pl
from .DataDescription import DataDescription
from .format import default_format_head, default_format_description
from typing import List, Callable, Dict, Any


def default_data_descriptor(name: str, desc: str) -> DataDescription:
    return DataDescription(name, desc)


class DataSet(DataDescription):
    def __init__(
        self,
        name: str,
        description: str,
        desc_formatter: Callable[[str], str] = default_format_description,
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
