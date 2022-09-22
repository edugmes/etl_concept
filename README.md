# Overview

This API demonstrates an ETL pipeline software tasks with two docker containers (MySQL database and FastAPI).

The data passes through the following stages: download csv content -> clean data -> store data into database -> query and
generate statistic of database data -> make data available via a restful API.

The original requirements are from [here](https://github.com/Profasee/python_engineer_assessment). If the link is off, refer
to the last section (**Requirements**) of this README file with a backup of the original content.

## Files overview
```
.
├── Dockerfile
├── README.md                   <-- this file :)
├── assessment
│   ├── __init__.py
│   ├── api
│   │   ├── __init__.py
│   │   ├── fastapi_schema.py   <-- fastAPI data schema
│   │   └── main.py             <-- fastAPI app and endpoint defintions
│   ├── database
│   │   ├── __init__.py
│   │   ├── data_schema.py      <-- SQLAlchemy table schema
│   │   ├── database_handler.py <-- PeopleDB class for creating, loading, and queryng stats from the database
│   │   └── db_config.py        <-- database configurations for SQLAlchemy
│   ├── datahandling
│   │   ├── __init__.py
│   │   ├── cleaning_utils.py   <-- tools for cleaning the data
│   │   └── csv_file_handler.py <-- CSVHandler class for downloading, saving and cleaning with cleaning_utils functions
│   ├── run.py                  <-- init script of asssessment container (e.g. download csv file)
│   ├── test.py                 <-- test container code
│   └── test_data.py            <-- some unittest for data cleaning
├── data                        <-- where csv files are automatically stored at container startup
│   ├── people.csv
│   └── people.json
├── docker-compose.yml          <-- updated containers definition
├── mysql-schemas
│   ├── person.sql              <-- data sql schema for Person table from SQLAlchemy
│   └── test.sql
└── requirements.txt            <-- updated pip requirements
```

## Assessment

The csv download and file saving happens automatically at `assessment` container startup (see `docker-compose.yml`
for details - it uses the `run.py` script).

`person.sql` schema was generated from MySQL, but it does not load the database. Loading is made at the container startup
metioned above.

As for the steps of the assessment:

1. CSV download and .csv/.json saving are done automatically at container startup and saved to `/data`.

2. `cleaning_utils.py` contains all the functions related to data cleaning.
Two types of data cleaning and people without interest data removal is done at `csv_file_handler.py -> CSVHandler -> clean_data`.
Unit tests are at `test_data.py`.


3. Database schema is stored at `mysql-schemas -> person.sql` and csv data loading is made at `database_handler.py -> PeopleDB -> save_from_dataframe`.

4. (And 5) Stats are made at `database_handler.py -> PeopleDB` and are available via api at `main.py -> people_stats`.


## The API

It has one endpoint at `"/people_stats` (e.g. localhost:8000/people_stats) and its Swagger documentation can be found at `/docs` (e.g. localhost:8000/docs).


## Testing

To run the unit tests for data cleaning, execute the following command under `assessment/`:

```
python -m unittest test_data.py
```

# Requirements

## Code test for python engineers

### Purpose

This is a test to demonstrate your understanding of data integrations, SQL databases, and ability to manipulate data into a format that is accessible for data scientists.

### Prerequisites

- Knowledge of python and the tools to integrate with APIs, process data, and interact with a file system and a SQL database.
- Knowledge of relational databases, including how to create tables, insert data, and query data. For the purpose of this test, we are using MySQL.
- Familiarity with Docker for container management, which we use through the Docker Compose tool. You will need Docker and Docker Compose installed on your development machine.
- Familiarity with Git for source control, and a github.com account which will be used for sharing your code.

We have included a test script that will ensure that the file system and MySQL database are set up correctly and accessible.

### Background

We have provided a Github repo containing:

- A **docker compose.yml** file that configures a container for the MySQL database and the script
- A **Dockerfile** to build and run the python script
- A **mysql-schemas** folder containing a test.sql file. You can add your sql schemas here.

### Test

To ensure the database is up and running, the following test can be run:

```
docker-compose up --build test
```

You should see output similar to the following:

```
Attaching to ml_data_engineer_assessment_test_1
test_1        | wait-for-it.sh: waiting 15 seconds for database:3306
test_1        | wait-for-it.sh: database:3306 is available after 0 seconds
test_1        | Found rows in database:  4
test_1        | Test Successful
ml_data_engineer_assessment_test_1 exited with code 0
```

### Assessment

The assessment consists of a series of small tasks to demonstrate your ability to perform the role of a python engineer at Profasee. We will be looking for both your ability to complete the tasks as well as the tools, data structures, python features, and code structure you use to accomplish the final result. Any python package needed can be added to the requirements.txt file. All code should be added to the `assessments` folder and be able to be run with the following command:
```
docker-compose up --build assessment
```

Complete the following tasks:

1. Download the CSV hosted at https://profasee-data-engineer-assessment-api.onrender.com/people.csv:
* Store the raw data in the `/data` directory.
* Convert the CSV to JSON format and store in the `/data` directory.
2. Inspect the data and list ways that the data can be cleaned up before being stored for a data science team to use.
* Write code to peform at least two types of the cleaning.
* Write unit tests to show the data cleaning functions work as expected.
* Write a function to filter people who have no interests.
3. Design a database schema to hold the data for the people in the CSV.
* Store the schema file in the `mysql-schemas` directory. These will be applied when the database container is created.
* Write code to load the data from the CSV into the database.
4. Create a function that uses the database tables to return the following stats of the people data:
* The minimum, maximum, and average age
* The city with the most people
* The top 5 most common interests
5. Create an API that serves an endpoint to return the data in Task 4.