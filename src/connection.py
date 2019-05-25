from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, Session

engine = create_engine('sqlite:///../sql/movies.db')
session = scoped_session(sessionmaker(bind=engine))  # type: Session
Base = declarative_base()
