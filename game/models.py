from sqlalchemy import Column, Integer, String, JSON, create_engine, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import Config

config = Config()


engine = create_engine(config.database_uri)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    username = Column(String)
    score = Column(Integer, default=0)
    height_score = Column(Integer, default=0)
    field = Column(JSON, default=list)
    theme = Column(String, default='classic')


Base.metadata.create_all(bind=engine)