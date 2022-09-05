import json

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

from csv_file_handler import CSVHandler
from data_schema import Person
from database_handler import PeopleDB

# from db_config import sql_schema_dump


def run():
    print("Hello, Profasee!")


if __name__ == "__main__":
    run()
    csv_handler = CSVHandler(
        "https://profasee-data-engineer-assessment-api.onrender.com/people.csv"
    )
    csv_handler.download_files()
    csv_handler.load_dataframe()
    # print(csv_handler.df.head())
    print(csv_handler.clean_data())

    people_db = PeopleDB()
    people_db.create()
    people_db.save_from_dataframe(csv_handler.df)
    print("\n\n\n")
    print("max age", people_db.max_age())
    print("min age", people_db.min_age())
    print("avg age", people_db.avg_age())
    print("freq city", people_db.most_frequent_city())
    print("most interest\n", people_db.top_x_interests(x=5))
