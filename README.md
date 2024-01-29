# c3d - create & comment `csv` data files 

A small library for post-processing of data (currently only csv) files:
**generating metadata and documentation of included data sets**

## Usage example 
A minimal working example looks like that:
```python
import os
import c3d as cdf

ds = cdf.DataSet("Data", "The description of the data set.")
    ds.append("Value_1", "The description of the value nr. 1.", 42)
    ds.append("Value_2", "The description of the second value.", 69)

# we decide to save all of our results here
results_f = "example_results"
if not os.path.exists(results_f):
    os.mkdir(results_f)

cdf.write_ds(ds, f"{results_f}/ex1.csv")
```
Here, we have a dataset called `Data` with a description. We also have two 
values that belong to the dataset. We also provide a description of the values.
Finally, we save it all in `ex1.csv` file that looks as follows:
```
# Data:
#    The description of the data set.
#
# Value_1:
#    The description of the value nr. 1.
#
# Value_2:
#    The description of the second value.
#
Value_1,Value_2
42,69

```

A more involved example (including metadata and some customisation) below:
```python
import os
import c3d as cdf
import polars as pl

if __name__ == "__main__":

    # ingest the raw data
    test_data = pl.read_csv("examples/test.csv")

    data_set = cdf.DataSet(
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

    # We can create the DataDescription here and pass it to our dataset. This
    # is not very convienent as we have to also make sure that the second arg
    # is a dataframe.
    data_set.append_data_raw(
        cdf.DataDescription("f2", "Second data set. Not very meanigful."),
        pl.DataFrame({"f2": test_data["second"]}),
    )

    # we decide to save all of our results here
    results_f = "example_results"
    if not os.path.exists(results_f):
        os.mkdir(results_f)

    # We will write the described dataset, including metadata.
    mdata = cdf.metadata(
        author="James Bond", time_stamp=True, count_lines=True
    )
    # We will also overwrite the comment sign to `--` like in `lua`.
    cdf.write_ds(
        data_set,
        f"{results_f}/ex2.csv",
        meta_data=mdata,
        comment_text="--",
    )
```
