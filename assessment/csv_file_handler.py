from pathlib import Path

import pandas as pd


class CSVHandler:
    def __init__(self, url) -> None:
        self.url = url
        self.base_path = (
            Path(__file__).parent.resolve().parent.resolve()
        )  # ../assessment
        self.df = None

    def download_files(self) -> None:
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
        self.df = pd.read_json(self.base_path.joinpath(f"data/people.json").resolve())

        return self.df
