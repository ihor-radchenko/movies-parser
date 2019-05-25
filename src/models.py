from sqlalchemy import Column, Integer, String
from connection import Base, engine


class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    unique_id = Column(String(191))
    name = Column(String(191))
    url = Column(String(191))
    poster_url = Column(String(191))
    country = Column(String(191))
    running_time = Column(String(191))
    release_year = Column(String(4))

    def __init__(self, *args, **kwargs):
        self.name = kwargs.get('name')
        self.unique_id = kwargs.get('unique_id')
        self.url = kwargs.get('url')
        self.poster_url = kwargs.get('poster_url')
        self.country = kwargs.get('country')
        self.running_time = kwargs.get('running_time')
        self.release_year = kwargs.get('release_year')


Base.metadata.create_all(engine)
