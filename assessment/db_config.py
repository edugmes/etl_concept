from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()
# engine_params = "sqlite:///foo.db"
user = "datatest"
password = "alligator"
root_pass = "root"
port = 3306
host = "database"
database = "datatestdb"
engine_params = f"mysql://{user}:{password}@{host}:{port}/{database}"
engine = create_engine(engine_params, echo=False)
