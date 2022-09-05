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
