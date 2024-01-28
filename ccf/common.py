from .DataSet import DataSet
from typing import Dict, Any


def write_ds(
    ds: DataSet,
    file_name: str,
    comment_text: str | None = None,
    header_entry_opts: Dict[str, Any] | None = None,
    header_desc_opts: Dict[str, Any] | None = None,
    entry_opts: Dict[str, Any] | None = None,
    desc_opts: Dict[str, Any] | None = None,
    meta_data: Dict[str, Any] | None = None,
):

    # Convert all to dictionaries, sice we cant do it in entry args
    if header_desc_opts is None:
        header_desc_opts = {}
    if header_entry_opts is None:
        header_entry_opts = {}
    if desc_opts is None:
        desc_opts = {}
    if entry_opts is None:
        entry_opts = {}

    if comment_text is not None:
        header_entry_opts["comment_text"] = comment_text
        header_desc_opts["comment_text"] = comment_text
        entry_opts["comment_text"] = comment_text
        desc_opts["comment_text"] = comment_text

    if meta_data is not None:
        header_entry_opts["meta_data"] = meta_data

    with open(file_name, mode="w") as file:
        file.write(
            ds.generate_header(
                header_entry_opts, header_desc_opts, entry_opts, desc_opts
            )
        )

    with open(file_name, mode="ab") as file:
        ds.data_.write_csv(file)
