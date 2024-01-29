#!/usr/bin/env python3

import os
import cccd as cdf


if __name__ == "__main__":

    ds = cdf.DataSet("Data", "The description of the data set.")
    ds.append("Value_1", "The description of the value nr. 1.", 42)
    ds.append("Value_2", "The description of the second value.", 69)

    # we decide to save all of our results here
    results_f = "example_results"
    if not os.path.exists(results_f):
        os.mkdir(results_f)

    cdf.write_ds(ds, f"{results_f}/ex1.csv")
