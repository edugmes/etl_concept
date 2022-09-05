from csv_file_handler import CSVHandler
from database_handler import PeopleDB

if __name__ == "__main__":
    # handle csv data
    csv_handler = CSVHandler(
        "https://profasee-data-engineer-assessment-api.onrender.com/people.csv"
    )
    # download csv if not already
    csv_handler.download_files()
    # load csv data into memory
    csv_handler.load_dataframe()
    # uncomment print below to see raw data
    # print(csv_handler.df.head())
    # peform certain data cleanning
    print(csv_handler.clean_data())

    # setup database
    people_db = PeopleDB()
    # create database table if if doesn't exist already
    people_db.create()
    # load the csv cleaned data into the database
    people_db.save_from_dataframe(csv_handler.df)

    # Uncomment lines below to get the stats at startup
    # print("max age ", people_db.max_age())
    # print("min age ", people_db.min_age())
    # print("avg age ", people_db.avg_age())
    # print("freq city ", people_db.most_frequent_city())
    # print("most interest ", people_db.top_x_interests(x=5))
