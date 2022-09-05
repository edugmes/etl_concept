# Overview

This API demonstrates an ETL pseudo pipeline with two docker containers (MySQL database and FastAPI).

The data passes through the following stages: download csv content -> data clean -> store in database -> query and
generate statistic of database data -> make data available via a restful API.

The original requirements are [here](https://github.com/Profasee/python_engineer_assessment).

## Files overview
```
.
├── Dockerfile
├── README.md                   <-- this file
├── assessment
│   ├── __init__.py
│   ├── cleaning_utils.py       <-- tools for cleaning the data
│   ├── csv_file_handler.py     <-- CSVHandler class for downloading, saving and cleaning with cleaning_utils functions
│   ├── data_schema.py          <-- SQLAlchemy table schema
│   ├── database_handler.py     <-- PeopleDB class for creating, loading, and queryng stats from the database
│   ├── db_config.py            <-- database configurations for SQLAlchemy
│   ├── fastapi_schema.py       <-- fastAPI data schema
│   ├── main.py                 <-- fastAPI app and endpoint defintions
│   ├── run.py                  <-- init script of asssessment container (e.g. download csv file)
│   ├── test.py                 <-- test container code
│   └── test_data.py            <-- some unittest for data cleaning
├── data                        <-- where csv files are autotically stored at container startup
│   ├── people.csv
│   └── people.json
├── docker-compose.yml          <-- updated containers defintion
├── mysql-schemas
│   ├── person.sql              <-- data schema for Person table from SQLAlchemy
│   └── test.sql
└── requirements.txt            <-- updated requirements
```

## Assessment

The csv download and file saving happens autotically at `assessment` container startup (see `docker-compose.yml`
for details - it uses the `run.py` script).

`person.sql` schema was generated from MySQL, but it does not load the database. Loading is made at the container startup
metioned above.

As for the steps of the assessment:

1. CSV download and .csv/.json saving is done automatically at container startup and saved to `/data`.

2. `cleaning_utils.py` contains all the functions related to data cleaning.
Two types of data cleaning and remove people without interest is done at `csv_file_handler.py -> CSVHandler -> clean_data`.
Unit tests are at `test_data.py`.


3. Database schema is stored at `mysql-schemas -> person.sql` and csv data load is made at `database_handler.py -> PeopleDB -> save_from_dataframe`.

4. (And 5) Stats are made at `database_handler.py -> PeopleDB` and are available via api at `main.py -> people_stats`.


## The API

It has one endpoint at `"/people_stats` (e.g. localhost:8000/people_stats) and its Swagger documentation can be found at `/docs` (e.g. localhost:8000/docs).
