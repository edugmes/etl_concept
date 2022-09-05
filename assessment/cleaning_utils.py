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


def update_column_types(df: pd.DataFrame, types_dict: dict = {}):
    """Given a dictionary in the form {'column name': 'new data type', ...} sets 'column_name' type to 'new data type' 

    :param df: The dataframe to update its columns types
    :param types_dict: dictionary in the form {'column name': 'new data type', ...}, defaults to {}
    :return: The updated dataframe
    """
    for col, data_type in types_dict.items():
        df[col] = df[col].astype(data_type)

    return df
