#!/usr/bin/env python3
import polars as pl
import os
from pycdf.DataSet import DataSet as ds
from pycdf.common import write_ds
from pycdf.metadata import metadata

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

    # Lets include some more metadata
    write_ds(
        data_set,
        results_f + "with_metadata.csv",
        meta_data=metadata(author="James Bond", time_stamp=True),
    )

    # Let's write the same but with the information about the amount of lines
    # in the header. It can be usefull if we have to skip these lines in some
    # data reader
    write_ds(
        data_set,
        results_f + "with_metadata.csv",
        meta_data=metadata(
            author="James Bond", time_stamp=True, count_lines=True
        ),
    )

    # lets use sepearate comment sign, "--" like in lua
    write_ds(
        data_set,
        results_f + "comment.csv",
        comment_text="--",
    )

