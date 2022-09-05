from typing import Union

import pandas as pd


def list_column_types(df: pd.DataFrame) -> list:
    """Return a list of (column name, data type) tuples of a dataframe

    :param df: The dataframe to inspect
    :return: List of tuples (column name, data type)
    """
    info = []
    for col, data in df.items():
        info.append((col, type(data[0])))
    return info


def update_column_types(df: pd.DataFrame, types_dict: dict = {}) -> pd.DataFrame:
    """Given a dictionary in the form {'column name': 'new data type', ...} sets 'column_name' type to 'new data type' 

    :param df: The dataframe to update its columns types
    :param types_dict: dictionary in the form {'column name': 'new data type', ...}, defaults to {}
    :return: The updated dataframe
    """
    for col, data_type in types_dict.items():
        df[col] = df[col].astype(data_type)

    return df


def rename_columns(
    df: pd.DataFrame, cols_dict: dict = {}, rules_to_apply: list = []
) -> pd.DataFrame:
    """Rename dataframe columns and apply function rule to transform the columns names (e.g. set them to lower case)

    :param df: The dataframe to rename and apply rules to columns names
    :param cols_dict: dictionary in the form {'old name': 'new name', ...} to rename columns names, defaults to {}
    :param rules_to_apply: list of functions to apply to the columns names, defaults to []
    :return: The renamed dataframe
    """
    df = df.rename(columns=cols_dict)

    new_cols = df.columns
    for rule in rules_to_apply:
        new_cols = list(map(rule, new_cols))

    df.columns = new_cols

    return df


def drop_null_columns(
    df: pd.DataFrame,
    null_percentage_threshold: float = 1.0,
    info_only: bool = True,
    cols_of_interest: Union[None, list] = None,
) -> Union[pd.DataFrame, pd.Series]:
    """Given a threshold of null elements, verify which columns are above this threshold and drop them.
    It's possible to only verify which are columns should be droped (no dataframe change) with info_only = True.
    If only some columns should be verified, they are specified with cols_of_interest.

    :param df: The dataframe to drop the columns with null elements above threshold
    :param null_percentage_threshold: The threshold of null elements from 0.0 to 1.0, defaults to 1.0
    :param info_only: If True, the dataframe isn't updated, defaults to True
    :param cols_of_interest: If set, only those columns are verified to be droped, defaults to None
    :return: Columns to be droped if info_only set to True, otherwise the updated dataframe
    """
    # df.info() shows non-null count for each column
    entries_count = len(df)

    # if dataframe shouldn't be updated, return the candidate columns to be removed ...
    if info_only:
        # calculate the percentage of total rows to be evaluated
        threshold = int(entries_count * null_percentage_threshold)

        # get info of how many null elements there are per column
        null_info = df.isnull().sum()

        # return the columns that are below threshold and, therefore, should be removed
        return null_info[null_info >= threshold]

    # ... otherwise remove the candidate columns and return the updated dataframe
    threshold = int(entries_count * (1 - null_percentage_threshold))
    # invert threshold for .dropn (i.e. how many non-null)
    df.dropna(
        axis="columns",
        how="any",
        thresh=threshold,
        subset=cols_of_interest,
        inplace=True,
    )

    return df


def drop_null_rows(
    df: pd.DataFrame,
    null_count: int,
    info_only: bool = True,
    cols_of_interest: Union[None, list] = None,
) -> pd.DataFrame:
    """Drop dataframe rows that have at least null_count null elements. Use cols_of_interest to restrict the drop
    verification only for such columns. If info_only == True, the dataframe is not updated, and the info to be droped
    is returned instead.

    :param df: The dataframe to drop rows that have at least null_count null elements
    :param null_count: The desired quantity of null elements to drop the rows
    :param info_only: If True, the dataframe isn't updated, defaults to True
    :param cols_of_interest: If set, only those columns are verified to be droped, defaults to None
    :return: Columns to be droped if info_only set to True, otherwise the updated dataframe
    """
    # .dropna removes rows that have less than 'thresh' non-null elements, so we calculate the other way around from
    # null_count: max(0, ...) to avoid negative values; len(df.columns) is the total number of columns; (null_count - 1)
    # is to make up for 'less than' of 'thresh'
    total = len(df.columns) if not cols_of_interest else len(cols_of_interest)
    thresh = max(0, total - (null_count - 1))

    if info_only:
        # fake removal for information purposes
        df_after_null_count_removal = df.dropna(
            axis="index", thresh=thresh, inplace=False, subset=cols_of_interest
        )
        # return only the values that should be removed by filtering original df with rows that are not (~) on the list
        # of rows to be kept
        return df[~df.index.isin(df_after_null_count_removal.index)]

    # actual removal
    df.dropna(axis="index", thresh=thresh, inplace=True, subset=cols_of_interest)

    return df
