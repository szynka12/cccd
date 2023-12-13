#!/usr/bin/env python3

# This script ingest the data for a regular simulation from different sources,
# annotates the data, and generates the selection of files containing
# macroscopic parameters and data

import os

import pandas as pd
from common import Data, write_data

if __name__ == "__main__":
    # ingest the raw data
    test_data = pd.read_csv("example_csv/test.csv")

    # add macroscopic parameters necessary to descibe your dataset, for example
    # Reynolds number and so on
    macroscopic_parameters = [
        Data(
            "name_macro_1",  # the name of the parameter
            "The description of macro parameter 1. It can be long. It will be"
            " wrapped internally to fit predefined size of the csv width.",
            20,  # value
        ),
    ]

    fields = [
        Data("f1", "first field", test_data["first"]),
        Data("f3", "third field", test_data["third"]),
    ]

    results_f = "example_results/"
    if not os.path.exists(results_f):
        os.mkdir(results_f)

    write_data(
        results_f + "ex_1_macro.csv",  # file name
        "Macroscopic paramteres",  # short  description
        macroscopic_parameters,  # data array.
    )
    write_data(
        results_f + "ex_1_fields.csv",
        "Fields",
        fields,
    )
