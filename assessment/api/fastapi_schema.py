from typing import Dict

from pydantic import BaseModel


class PeopleStatsOut(BaseModel):
    max_age: int
    min_age: int
    avg_age: float
    city_with_most_people: str
    top_5_interests: list
