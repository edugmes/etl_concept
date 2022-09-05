from sqlalchemy import Column, Integer, MetaData, String, create_engine

from db_config import Base


class Person(Base):
    __tablename__ = "person"

    id = Column(Integer, primary_key=True)
    title = Column(String(10))
    name = Column(String(100))
    age = Column(Integer)
    city = Column(String(100))
    interest1 = Column(String(100))
    interest2 = Column(String(100))
    interest3 = Column(String(100))
    interest4 = Column(String(100))
    phone_number = Column(String(50))

    def __repr__(self):
        return f"<Person(title='{self.title}', name='{self.name}', age='{self.age}')>"
