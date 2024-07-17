from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# This can be easily changed to implement other database systems
DB_URL = "sqlite:///dataset.db"

# The engine must have the "check_same_thread" flag setted to False in order to to allow
# FastAPI to do its own thing regarding thread calls
# NOTE - This is not necessary for other DB systems
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})

# Creating a unique session to be "shared" with all endpoints
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Creating the DB
Base = declarative_base()
