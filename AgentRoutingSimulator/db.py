from sqlalchemy import JSON, VARCHAR, Column, DateTime, Float, Integer, String, create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
_engine = None

class Agent(Base):
    __tablename__ = "Agent"
    # Hier muss vielleicht etwas verändert werden bezüglich mapping zwischen id(uuid) und id(db)
    id = Column(Integer, primary_key=True, autoincrement=True)
    position_x = Column(Float)
    position_y = Column(Float)
    config = Column(JSON)


class Simulation(Base):
    __tablename__ = "Entity"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    start_datetime = Column(DateTime)
    end_datetime = Column(DateTime)
    config = Column(JSON)


class Stat(Base):
    __tablename__ = "Stat"

    id = Column(Integer, primary_key=True)
    step = Column(Integer)
    value = Column(JSON)


class StatType(Base):
    __tablename__ = "StatType"

    id = Column(Integer, primary_key=True)
    name = Column(String)


def get_session(connection_string):
    global _engine

    if _engine is None:
        _engine = create_engine(connection_string, encoding='UTF-8', echo=True)
        Base.metadata.create_all(_engine)
    
    return Session(_engine)
