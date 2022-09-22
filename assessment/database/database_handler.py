from typing import Union

import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy.sql import desc, func

from database.data_schema import Person
from database.db_config import Base, engine


class PeopleDB:
    def create(self):
        """Create the database schema to the database engine"""
        Base.metadata.create_all(engine)

    def save_from_dataframe(self, df: pd.DataFrame) -> None:
        """Take df data and store it in one command to the database engine

        :param df: The dataframe to extract data
        """
        df.to_sql(
            name=Person.__tablename__,
            con=engine,
            if_exists="replace",  # 'append', 'replace' or 'fail' available
            method="multi",
            index=True,
            index_label="id",
        )

    def max_age(self) -> int:
        """Open a session to query the maximum age of people

        :return: The maximum age
        """
        session = Session(engine)
        person_obj = session.query(Person).order_by(Person.age.desc()).first()
        session.close()

        return person_obj.age

    def min_age(self) -> int:
        """Open a session to query the minimum age of people

        :return: The minimum age
        """
        session = Session(engine)
        person_obj = session.query(Person).order_by(Person.age).first()
        session.close()

        return person_obj.age

    def avg_age(self) -> float:
        """Open a session to query the average age of people

        :return: The average age
        """
        session = Session(engine)
        result = session.query(func.avg(Person.age).label("avg_age")).first()
        session.close()

        return result[0]

    def top_x_interests(self, x: int = 1, as_dict: bool = False) -> Union[dict, list]:
        """Select the top x interests among interest 1, 2, 3, and 4

        :param x: How many interests to get, defaults to 1
        :param as_dict: If full dictionary should be returned, defaults to False
        :return: Dictionary with {'interest': 'quantity', ...} if as_dict == True, otherwise just the list of top x interests
        """
        session = Session(engine)
        # select all interests of the database and save them into a dataframe
        df = pd.read_sql(
            session.query(
                Person.interest1, Person.interest2, Person.interest3, Person.interest4
            ).statement,
            session.bind,
        )
        session.close()

        # filter the top interests using pandas instead of sqlalchemy
        df_result = (
            pd.concat(
                [df["interest1"], df["interest2"], df["interest3"], df["interest4"]]
            )
            .value_counts()
            .sort_values(ascending=False)
        )

        # select x interests of the numpy array
        top_interest = df_result[:x]

        # store the interests in a dictionary
        result = {}
        for index in top_interest.index:
            result[index] = top_interest[index]

        if as_dict:
            return result
        return list(result.keys())

    def most_frequent_city(self) -> str:
        """Query top city of most people

        :return: The most frequent city of the data
        """
        session = Session(engine)
        result = (
            session.query(func.count(Person.city).label("person_count"), Person.city)
            .group_by(Person.city)
            .order_by(desc("person_count"))
        )
        session.close()

        return result[0][1]
