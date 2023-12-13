import textwrap as tw
import pandas as pd
import numpy as np


class Data:
    def __init__(self, name: str, description: str, data, shift: int = 0):
        self.name_ = name
        self.description_ = description

        if shift > 0:
            self.data_ = (
                data.shift(1).append(data.iloc[[-1]]).reset_index(drop=True)
            )
        else:
            self.data_ = data

        if isinstance(self.data_, pd.Series):
            self.data_.rename(self.name_, inplace=True)

    def desc_entry(self) -> str:
        indent_text = "#    "
        desc_wrapped = tw.fill(
            tw.dedent(self.description_),
            width=80,
            initial_indent=indent_text,
            subsequent_indent=indent_text,
            break_long_words=False,
            expand_tabs=True,
            tabsize=4,
        )
        return "# " + self.name_ + ":\n" + desc_wrapped + "\n#\n"


def find_data_in_list(name: str, data_list) -> Data:
    el = [x for x in data_list if x.name_ == name]
    if el:
        return el[0]
    else:
        raise NameError(name + " not found in list!")


def ensure_DataFrame(entry):
    if isinstance(entry.data_, (pd.DataFrame, pd.Series)):
        return entry.data_

    # scalar data
    if not isinstance(entry.data_, (list, tuple, np.ndarray, pd.Series)):
        return pd.DataFrame(data={entry.name_: entry.data_}, index=[0])

    # lists
    return pd.DataFrame(data={entry.name_: entry.data_})


def construct_DataFrame(param_list):
    return pd.concat([ensure_DataFrame(x) for x in param_list], axis=1)


def construct_header(param_list):
    return "".join([x.desc_entry() for x in param_list])


def write_data(file: str, description: str, param_list):
    # get the header, compute the information about it
    head = construct_header(param_list)

    indent_text = "#    "
    description = tw.fill(
        tw.dedent(description),
        width=80,
        initial_indent=indent_text,
        subsequent_indent=indent_text,
        break_long_words=False,
        expand_tabs=True,
        tabsize=4,
    )
    n_lines = head.count("\n") + description.count("\n")
    head = (
        "# Header contains {} lines\n".format(n_lines + 6)
        + "# Description of the dataset:\n"
        + description
        + "\n#\n"
        + "# Data entries are described below:\n"
        + "#\n"
        + head
    )

    df = construct_DataFrame(param_list)

    with open(file, "w") as file:
        file.write(head)
        df.to_csv(file, index=False)
