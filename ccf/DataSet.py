import polars as pl
from DataDescription import DataDescription
from typing import List


class DataSet:
    def __init__(self, name: str, description: str):
        self.name_: str = name
        self.description_: str = description

        self.data_descriptions_: List[DataDescription] = []
        self.data: pl.DataFrame = pl.DataFrame()
