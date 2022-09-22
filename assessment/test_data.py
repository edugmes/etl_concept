import unittest

import numpy
import pandas as pd
from pandas.testing import assert_frame_equal

import datahandling.cleaning_utils as clut
from datahandling.csv_file_handler import CSVHandler


class DataTests(unittest.TestCase):
    def setUp(self):
        csv_handler = csv_handler = CSVHandler(
            "https://profasee-data-engineer-assessment-api.onrender.com/people.csv"
        )
        csv_handler.download_files()
        csv_handler.load_dataframe()

        self.dirty_df = csv_handler.df.copy(deep=True)
        self.original_types = [
            ("Name", str),
            ("Age", numpy.int64),
            ("City", str),
            ("Interest1", str),
            ("Interest2", str),
            ("Interest3", str),
            ("Interest4", str),
            ("PhoneNumber", str),
        ]

        self.clean_df = csv_handler.clean_data()

    def test_original_types_expected(self):
        assert clut.list_column_types(self.dirty_df) == self.original_types

    def test_column_name_change(self):
        df = clut.rename_columns(self.dirty_df, cols_dict={"PhoneNumber": "phone"})
        assert df.columns[-1] == "phone"

    def test_column_name_to_upper(self):
        df = clut.rename_columns(self.dirty_df, rules_to_apply=[lambda x: x.upper()])
        assert df.columns[-1] == "PHONENUMBER"

    def test_interest1_column_drop_for_null_values(self):
        # check column present before
        self.assertIn("interest1", self.clean_df.columns)
        dropped_interest_1 = self.clean_df.loc[:, self.clean_df.columns != "interest1"]
        # check column is not present anymore
        self.assertNotIn("interest1", dropped_interest_1.columns)

        droped_df = clut.drop_null_columns(self.clean_df, 0.7, info_only=False)

        assert_frame_equal(droped_df, dropped_interest_1)
