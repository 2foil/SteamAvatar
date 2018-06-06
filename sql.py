from sqlalchemy import Column, String, create_engine, Integer,ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Game(Base):
    __tablename__ = 'game'
    id = Column(String, primary_key=True)
    name = Column(String)
    avatars = relationship('Avatar')

class Avatar(Base):
    __tablename__ = 'avatar'

    id = Column(Integer, primary_key=True)
    url = Column(String)
    game_id = Column(String, ForeignKey('game.id'))

engine = create_engine('sqlite:///avatar.sqlite')
Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)