from sqlalchemy import create_engine, Column, Integer, String, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import Config

config = Config()

Base = declarative_base()

class User(Base):
    __tablename__ = 'users_game'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    score = Column(Integer)
    field = Column(ARRAY(Integer))

engine = create_engine(config.database_uri)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)