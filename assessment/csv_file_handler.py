from pathlib import Path

import pandas as pd

from cleaning_utils import (
    data_to_lower_case,
    drop_null_columns,
    drop_null_rows,
    rename_columns,
    split_titles_from_name,
    trim_data,
    update_column_types,
)


class CSVHandler:
    def __init__(self, url) -> None:
        self.url = url
        self.base_path = (
            Path(__file__).parent.resolve().parent.resolve()
        )  # ../assessment
        self.df = None

    def download_files(self) -> None:
        """Download csv files to .csv and .json formats if '../data/' has no files already
        """
        csv_name = "people.csv"
        json_name = "people.json"

        if self.base_path.joinpath(f"data/{csv_name}").resolve().is_file():
            print("File already exists, nothing to do.")
        else:
            print("File doesn't exist. Downloading and saving files.")
            data_path = self.base_path.joinpath("data").resolve()
            data_path.mkdir(parents=True, exist_ok=True)

            df = pd.read_csv(self.url)
            df.to_csv(data_path.joinpath(csv_name))
            df.to_json(data_path.joinpath(json_name))

    def load_dataframe(self) -> pd.DataFrame:
        """Load '../data/people.json' file content to CSVHandler 'df' attribute

        :return: The dataframe
        """
        self.df = pd.read_json(self.base_path.joinpath(f"data/people.json").resolve())

        return self.df

    def clean_data(self):
        """Apply at least two data cleaning functions. Specifically:
        a - change "Age" type to "int" (no need for float)
        b - rename "PhoneNumber" to "phone_number"
        c - set all columns names to lower case
        d - set all string values to lower case
        e - trim all string values (' swimming', 'swimming ', and 'swimming' should be the same thing)
        f - try to drop entire columns that have at least 80% (0.8) of values as null
        g - drop rows of people that have no interest

        Cleaning suggestions:
        - use .fillnan to fill null values with more meaningful values for each column
        - apply some mask to phone_number (e.g. add +1 to all numbers with it - if all from USA or replace '.' for '-')
        :return: A cleaned dataframe
        """
        # a (description above)
        self.df = update_column_types(self.df, {"Age": int})
        # b (description above)
        self.df = rename_columns(
            self.df,
            {"PhoneNumber": "phone_number"},
            rules_to_apply=[lambda x: x.lower()],
        )
        print(self.df.head())
        # c (description above)
        self.df = data_to_lower_case(self.df)
        # d (description above)
        self.df = trim_data(self.df)
        # e (description above)
        self.df = split_titles_from_name(self.df)
        # f (description above)
        self.df = drop_null_columns(
            self.df, null_percentage_threshold=0.8, info_only=False
        )
        # g (description above)
        self.df = drop_null_rows(
            self.df,
            null_count=4,
            info_only=False,
            cols_of_interest=["interest1", "interest2", "interest3", "interest4"],
            # cols_of_interest=["interest2", "interest3", "interest4"],
        )

        return self.df
