from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()
engine_params = "sqlite:///foo.db"
engine = create_engine(engine_params, echo=False)
