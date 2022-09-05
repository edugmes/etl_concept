from fastapi import FastAPI

from database_handler import PeopleDB
from fastapi_schema import PeopleStatsOut

app = FastAPI(
    title="ETLConceptAPI",
    description="""This API demonstrates an ETL pseudo pipeline with two docker containers (MySQL database and FastAPI).
         The data passes through the following stages: download csv content -> data clean -> store in database -> query and
         generate statistic of database data -> make data available via a restful API.""",
    version="1.0.0",
)


@app.get(
    "/people_stats",
    response_model=PeopleStatsOut,
    tags=["PeopleStats"],
)
def people_stats():
    """Get people stats: max, min, and average age; city with most people; and their top 5 interests

    :return: A dictionary with the mentioned stats
    """
    people_db = PeopleDB()

    max_age = people_db.max_age()
    min_age = people_db.min_age()
    avg_age = people_db.avg_age()
    city_with_most_people = people_db.most_frequent_city()
    top_5_interests = people_db.top_x_interests(x=5)

    return {
        "max_age": max_age,
        "min_age": min_age,
        "avg_age": avg_age,
        "city_with_most_people": city_with_most_people,
        "top_5_interests": top_5_interests,
    }
