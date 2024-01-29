from typing import Dict, Any

from enum import StrEnum
from datetime import datetime


class MDataNames(StrEnum):
    author = "Author"
    s_time = "Time (saved)"
    n_lines = "N. of lines in the header"


def metadata(
    author: str | None = None,
    time_stamp: bool = False,
    count_lines: bool = False,
) -> Dict[str, Any]:

    mdata = {}
    M = MDataNames

    if author is not None:
        mdata[M.author] = author

    if time_stamp:
        mdata[M.s_time] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    mdata[M.n_lines] = count_lines

    return mdata
