import csv

from csv_file_handler import CSVHandler


def run():
    print("Hello, Profasee!")


if __name__ == "__main__":
    run()
    csv_handler = CSVHandler(
        "https://profasee-data-engineer-assessment-api.onrender.com/people.csv"
    )
    csv_handler.download_files()
    csv_handler.load_dataframe()
    print(csv_handler.df.head())
