import unittest

import numpy
import pandas as pd
from pandas.util.testing import assert_frame_equal

import cleaning_utils as clut
from csv_file_handler import CSVHandler


class DataTests(unittest.TestCase):
    def setUp(self):
        csv_handler = CSVHandler(
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

    def test_original_types_expected(self):
        assert clut.list_column_types(self.dirty_df) == self.original_types

    def test_column_name_change(self):
        df = clut.rename_columns(self.dirty_df, cols_dict={"PhoneNumber": "phone"})
        assert df.columns[-1] == "phone"

    def test_column_name_to_lower(self):
        df = clut.rename_columns(self.dirty_df, rules_to_apply=[lambda x: x.upper()])
        assert df.columns[-1] == "PHONENUMBER"
