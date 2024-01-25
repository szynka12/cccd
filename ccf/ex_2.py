#!/usr/bin/env python3

import polars as pl
import os
from DataDescription import DataDescription
from DataSet import DataSet
from common import write_ds

if __name__ == "__main__":

    # ingest the raw data
    test_data = pl.read_csv("example_csv/test.csv")

    data_set = DataSet(
        "Test data set description",
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin"
        " placerat augue vel diam elementum vestibulum rhoncus volutpat ipsum."
        " Maecenas pulvinar elit eget ullamcorper euismod. Etiam pretium vitae"
        " neque vitae mollis. Morbi dignissim tincidunt enim a ultrices. Donec"
        " iaculis sagittis est, mollis vulputate massa luctus sit amet. Proin"
        " porta lectus non purus euismod condimentum. Aenean in nisi vel odio"
        " semper dapibus nec in nisi.",
    )

    data_desc_1 = DataDescription("1st data", "This is a description")
    data_set.append_data_raw(
        data_desc_1,
        pl.DataFrame({data_desc_1.column_name(): test_data["first"]}),
    )

    data_set.append(
        "2nd data",
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        test_data["second"],
    )

    print(data_set.generate_header({"write_lines": True}))

    results_f = "example_results/"
    if not os.path.exists(results_f):
        os.mkdir(results_f)

    write_ds(
        data_set,
        results_f + "ex_2.csv",
    )
