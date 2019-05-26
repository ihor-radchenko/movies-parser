from sqlalchemy import Column, Integer, String
from connection import Base, engine


class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(191))
    url = Column(String(191), unique=True)
    poster_url = Column(String(191))
    country = Column(String(191))
    running_time = Column(String(191))
    release_year = Column(String(4))
    site = Column(String(191))
    omdbapi_parsed = Column(Integer, default=0)

    def __init__(self, *args, **kwargs):
        self.name = kwargs.get('name')
        self.url = kwargs.get('url')
        self.poster_url = kwargs.get('poster_url')
        self.country = kwargs.get('country')
        self.running_time = kwargs.get('running_time')
        self.release_year = kwargs.get('release_year')
        self.site = kwargs.get('site')


class Country(Base):
    __tablename__ = 'countries'

    id = Column(Integer, primary_key=True)
    name = Column(String(191))
    alpha_2_code = Column(String(2))
    alpha_3_code = Column(String(3))
    population = Column(Integer)
    flag_file_name = Column(String(191))
    flag_external_url = Column(String(191))

    def __init__(self, name, alpha_2_code, alpha_3_code, population, flag_file_name, flag_external_url):
        self.name = name
        self.alpha_2_code = alpha_2_code
        self.alpha_3_code = alpha_3_code
        self.population = population
        self.flag_file_name = flag_file_name
        self.flag_external_url = flag_external_url


Base.metadata.create_all(engine)
