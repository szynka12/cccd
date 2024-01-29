import polars as pl
from .DataDescription import DataDescription
from .format import f_description, f_entry
from typing import List, Callable, Dict, Any


def default_data_descriptor(name: str, desc: str) -> DataDescription:
    return DataDescription(name, desc)


class DataSet(DataDescription):
    def __init__(
        self,
        name: str,
        description: str,
        desc_formatter: Callable[[str], str] = f_description,
        entry_formatter: Callable[[str, str], str] = f_entry,
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

        if "append_text" in entry_opts:
            header_entry_opts["append_text"] += data_entries_text
        else:
            header_entry_opts["append_text"] = data_entries_text

        return super().to_text(header_entry_opts, header_desc_opts)

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
