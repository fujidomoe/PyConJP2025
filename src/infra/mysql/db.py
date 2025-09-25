import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session as ORMSession
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

username = os.environ["DB_USER"]
password = os.environ["DB_PASS"]
hostname = os.environ["DB_HOST"]
database = os.environ["DB_NAME"]

dsl = f"mysql+pymysql://{username}:{password}@{hostname}/{database}?charset=utf8mb4"
engine = create_engine(
    dsl,
    echo=False,
    pool_pre_ping=True,
    isolation_level="READ_COMMITTED",
    future=True,
)

session = scoped_session(
    sessionmaker(
        bind=engine,
        class_=ORMSession,
        expire_on_commit=False,
    )
)
Base = declarative_base()
