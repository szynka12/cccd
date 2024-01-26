# ccf - Comment CSV file
A small library for post-processing of csv files: **generating metadata and documentation of included data sets**

## Usage example

```python
import polars as pl
import os
from ccf.DataSet import DataSet as ds
from ccf.common import write_ds

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

data_set.append("f2", "Much less meaningful data, oh no!", test_data["second"])

# we decide to save all of our results here
results_f = "example_results/"
if not os.path.exists(results_f):
    os.mkdir(results_f)

# Let's write the default version
write_ds(data_set, results_f + "defaults.csv")
```
which produces the following `csv`:
```
# This is the dataset nr. 1:
#
#    The description of the data set and each field can be long. It will be
#    wrapped anyway. I could even put Lorem Ipsum here.
#
# Data entries are described below:
#
# f1:
#    This data describes f1 and is very meaningful!
#
# f2:
#    Much less meaningful data, oh no!
#
f1,f2
1.0,2
2.3,3
```

## Customisation
### Number of lines in the header
Let's write the same but with the information about the amount of lines
in the header.
```python
write_ds(data_set, results_f + "with_lines.csv", write_lines=True)
```
It can be usefull if we have to skip these lines in some
data reader. The result looks like that
```
# This is the dataset nr. 1:
#
# - The header contains 15 lines
#
#    The description of the data set and each field can be long. It will be
#    wrapped anyway. I could even put Lorem Ipsum here.
#
# Data entries are described below:
#
# f1:
#    This data describes f1 and is very meaningful!
#
# f2:
#    Much less meaningful data, oh no!
#
f1,f2
1.0,2
2.3,3
```
### Comment sign
We can also use different comment sign, for example `--` like in lua
```python
write_ds(data_set, results_f + "comment.csv", write_lines=True, comment_text="--")
```
resulting in 
```
-- This is the dataset nr. 1:
--
-- - The header contains 15 lines
--
--    The description of the data set and each field can be long. It will be
--    wrapped anyway. I could even put Lorem Ipsum here.
--
-- Data entries are described below:
--
-- f1:
--    This data describes f1 and is very meaningful!
--
-- f2:
--    Much less meaningful data, oh no!
--
f1,f2
1.0,2
2.3,3
```

### Overwriting the description of the whole dataset
Finally lets completely change the format by adding information about the
author at the begining of the file. In order to do that we have to
redefine the entry_formatter of DataSet class. It is a functor, so we
define new function
```python
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

```
Now using our new function:
```python
data_set2 = ds(
    "This is the dataset nr. 2",
    "The description of the data set and each field can be long. It will"
    " be wrapped anyway. I could even put Lorem Ipsum here.",
    entry_formatter=with_author,  # The formatter should be passed here
)

data_set2.append("macro parameter name with space", "It is important to document stuff.", 42)

write_ds( data_set2, results_f + "with_author.csv", write_lines=True,
    header_entry_opts={"author_name": "James Bond"},
)
```
Not the best code ever writen, but it does the job: 
```
# This is the dataset nr. 1:
#
# - Author: James Bond
#
# - The header contains 12 lines
#
#    The description of the data set and each field can be long. It will be
#    wrapped anyway. I could even put Lorem Ipsum here.
#
# Data entries are described below:
#
# macro parameter name with space:
#    It is important to document stuff.
#
macro parameter name with space
42
```
