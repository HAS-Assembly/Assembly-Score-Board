from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
import datetime

from database import Base


class Game1(Base):
    __tablename__ = "game1"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    score = Column(Integer, nullable=True)
    session_id = Column(Integer, nullable=False)


class Game2(Base):
    __tablename__ = "game2"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    score = Column(Integer, nullable=True)
    session_id = Column(Integer, nullable=False)


class Game3(Base):
    __tablename__ = "game3"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    score = Column(Integer, nullable=True)
    session_id = Column(Integer, nullable=False)


class ApiLog(Base):
    __tablename__ = "api_log"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, nullable=True)
    name = Column(String, nullable=True)
    score = Column(Integer, nullable=True)
    session_id = Column(Integer, nullable=False)
    game = Column(Integer, nullable=False)
    ip = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.now)
    endpoint = Column(String, nullable=False)


class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    token = Column(Integer, nullable=False)


class TokenLog(Base):
    __tablename__ = "token_log"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    token_delta = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.now)
