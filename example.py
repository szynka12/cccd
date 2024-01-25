#!/usr/bin/env python3
import polars as pl
import os
from ccf.DataSet import DataSet as ds
from ccf.common import write_ds

if __name__ == "__main__":

    # ingest the raw data
    test_data = pl.read_csv("example_csv/test.csv")

    data_set = ds(
        "This is the dataset nr. 1",
        "The description of the data set and each field can be long. It will"
        " be wrapped anyway. I could even put Lorem Ipsum here.",
    )

    # lets describe the raw data that we have
    data_set.append(
        "f1",  # name
        "This data describes f1 and is very meaningful!",  # description
        test_data[
            "first"
        ],  # value, currently it should be a Series or something like that
    )

    data_set.append(
        "f2",
        "Much less meaningful data, oh no!",
        test_data["second"],
    )

    # we decide to save all of our results here
    results_f = "example_results/"
    if not os.path.exists(results_f):
        os.mkdir(results_f)

    # Let's write the default version
    write_ds(data_set, results_f + "defaults.csv")

    # Let's write the same but with the information about the amount of lines
    # in the header. It can be usefull if we have to skip these lines in some
    # data reader
    write_ds(data_set, results_f + "with_lines.csv", write_lines=True)

    # lets use sepearate comment sign, "--" like in lua
    write_ds(
        data_set,
        results_f + "comment.csv",
        write_lines=True,
        comment_text="--",
    )

    # Finally lets completely change the format by adding information about the
    # author at the begining of the file. In order to do that we have to
    # redefine the entry_formatter of DataSet class. It is a functor, so we
    # define new function
    def with_author(
        name: str,  # name of the dataset
        formatted_description: str,  # description of the dataset
        author_name: str | None = None,
        n_lines_data: int | None = None,
        write_lines: bool = False,
        comment_text: str = "#",
    ) -> str:

        line_info = (
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

        author_info = (
            f"{comment_text} - Author: {author_name}\n{comment_text}\n"
            if author_name is not None
            else ""
        )

        return (
            f"{comment_text} {name}:\n"
            + f"{comment_text}\n"
            + author_info
            + line_info
            + f"{formatted_description}{comment_text}\n"
            + f"{comment_text} Data entries are described below:\n"
            + f"{comment_text}\n"
        )

    # Not the best code I've written but it will do the job. We still have to
    # create new data set for that operation.

    data_set2 = ds(
        "This is the dataset nr. 1",
        "The description of the data set and each field can be long. It will"
        " be wrapped anyway. I could even put Lorem Ipsum here.",
        entry_formatter=with_author,
    )

    # lets again describe the data
    data_set2.append(
        "macro parameter name with space",
        "It is important to document stuff.",
        42,
    )

    write_ds(
        data_set2,
        results_f + "with_author.csv",
        write_lines=True,
        header_entry_opts={"author_name": "James Bond"},
    )
