from sqlalchemy import ForeignKey, JSON, Column, DateTime, Float, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
_engine = None


class Simulation(Base):
    __tablename__ = "Simulation"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    start_datetime = Column(DateTime)
    end_datetime = Column(DateTime)
    current_time_step = Column(Integer)
    current_message_count = Column(Integer)
    config = Column(JSON)

    stats = relationship("Stat", back_populates="simulation")
    agents = relationship("Agent", back_populates="simulation")
    connections = relationship("Connection", back_populates="simulation")


class Agent(Base):
    __tablename__ = "Agent"
    # Hier muss vielleicht etwas verändert werden bezüglich mapping zwischen id(uuid) und id(db)
    id = Column(Integer, primary_key=True, autoincrement=True)
    position_x = Column(Float)
    position_y = Column(Float)
    config = Column(JSON)

    simulation = relationship("Simulation", back_populates="agents")
    simulation_id = Column(Integer, ForeignKey("Simulation.id"))


class Connection(Base):
    __tablename__ = "Connection"
    # Hier muss vielleicht etwas verändert werden bezüglich mapping zwischen id(uuid) und id(db)
    id = Column(Integer, primary_key=True, autoincrement=True)
    config = Column(JSON)

    simulation = relationship("Simulation", back_populates="connections")
    simulation_id = Column(Integer, ForeignKey("Simulation.id"))


class StatType(Base):
    __tablename__ = "StatType"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    stats = relationship("Stat", back_populates="stat_type")


class Stat(Base):
    __tablename__ = "Stat"

    id = Column(Integer, primary_key=True)
    step = Column(Integer)
    value = Column(JSON)

    stat_type = relationship("StatType", back_populates="stats")
    simulation = relationship("Simulation", back_populates="stats")

    stat_type_id = Column(Integer, ForeignKey("StatType.id"))
    simulation_id = Column(Integer, ForeignKey("Simulation.id"))


