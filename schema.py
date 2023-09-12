from pydantic import BaseModel, validator
from fastapi import HTTPException, status


# session_id: int, name: str, student_id: int, score: int, difficulty: int,
class UploadGame1(BaseModel):
    session_id: int
    name: str
    student_id: int
    score: int
    difficulty: int

    @validator('difficulty')
    def check_difficulty(cls, v):
        if v not in [1, 3]:
            raise ValueError('잘못된 difficulty 입니다.')
        return v

    @validator('score')
    def check_score(cls, v, values):
        if v < 0:
            raise ValueError('잘못된 score 입니다.')
        return v


class UploadGame(BaseModel):
    session_id: int
    name: str
    student_id: int
    score: int

    @validator('score')
    def check_score(cls, v, values):
        if v < 0:
            raise ValueError('잘못된 score 입니다.')
        return v


class SessionID(BaseModel):
    game: int
    name: str
    student_id: int

    @validator('game')
    def check_game(cls, v):
        if v not in [1, 2, 3]:
            raise ValueError('잘못된 game 입니다.')
        return v


class Scores(BaseModel):
    game1: list[dict[str, int | str]]
    game2: list[dict[str, int | str]]
    game3: list[dict[str, int | str]]


class UserRequest(BaseModel):
    student_id: int
    name: str
    token_to_add: int
    admin_password: str
