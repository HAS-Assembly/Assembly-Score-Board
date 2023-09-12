import http
import random

from passlib.context import CryptContext
from sqlalchemy.orm import Session
import pandas as pd
from fastapi import HTTPException, Depends
from schema import UploadGame1, SessionID, Scores, UserRequest

from models import Game1, Game2, Game3, User, TokenLog

from database import get_db
from starlette.config import Config

config = Config('.env')

admin_password = config('ADMIN_PASSWORD')


def get_game1(db: Session):
    df = pd.read_sql_table('game1', con=db.bind).sort_values(by='score', ascending=False).head(10)
    df = df[df['score'] != 0]
    return df


def get_game2(db: Session):
    df = pd.read_sql_table('game2', con=db.bind).sort_values(by='score', ascending=False).head(10)
    df = df[df['score'] != 0]
    return df


def get_game3(db: Session):
    df = pd.read_sql_table('game3', con=db.bind).sort_values(by='score', ascending=False).head(10)
    df = df[df['score'] != 0]
    return df


def add_game1(db: Session, _add_game: UploadGame1):
    game = db.query(Game1).filter(Game1.session_id == _add_game.session_id).first()
    if game:
        if _add_game.difficulty == 3 and _add_game.score > 600:
            raise HTTPException(status_code=http.HTTPStatus.BAD_REQUEST, detail="invalid score")
        elif _add_game.difficulty == 1 and _add_game.score > 400:
            raise HTTPException(status_code=http.HTTPStatus.BAD_REQUEST, detail="invalid score")
        elif _add_game.student_id != game.student_id or _add_game.name != game.name:
            raise HTTPException(status_code=http.HTTPStatus.BAD_REQUEST, detail="invalid student id or name")
        else:
            game.score = _add_game.score
    else:
        raise HTTPException(status_code=http.HTTPStatus.FORBIDDEN, detail="invalid session id")
    db.commit()


def add_game2(db: Session, _add_game: UploadGame1):
    game = db.query(Game2).filter(Game2.session_id == _add_game.session_id).first()
    if game:
        if _add_game.student_id != game.student_id or _add_game.name != game.name:
            raise HTTPException(status_code=http.HTTPStatus.BAD_REQUEST, detail="invalid student id or name")
        game.score = _add_game.score
    else:
        raise HTTPException(status_code=http.HTTPStatus.FORBIDDEN, detail="invalid session id")
    db.commit()


def add_game3(db: Session, _add_game: UploadGame1):
    game = db.query(Game3).filter(Game3.session_id == session_id).first()
    if game:
        if _add_game.student_id != game.student_id or _add_game.name != game.name:
            raise HTTPException(status_code=http.HTTPStatus.BAD_REQUEST, detail="invalid student id or name")
        game.score = _add_game.score
    else:
        raise HTTPException(status_code=http.HTTPStatus.FORBIDDEN, detail="invalid session id")
    db.commit()


def make_session_id(db, _make_session_id: SessionID):
    game_dict = {1: Game1, 2: Game2, 3: Game3}

    user = db.query(User).filter(User.student_id == _make_session_id.student_id).first()
    if user:
        if user.name != _make_session_id.name:
            raise HTTPException(status_code=http.HTTPStatus.BAD_REQUEST, detail="invalid name or student id")
        if not (user.token > 0):
            raise HTTPException(status_code=http.HTTPStatus.FORBIDDEN, detail="token 부족")
        user.token -= 1
    else:
        raise HTTPException(status_code=http.HTTPStatus.UNAUTHORIZED, detail="no such user")

    session_id = random.randint(1000, 9999) + (
            db.query(game_dict[_make_session_id.game]).count() + 1) * 100000 + _make_session_id.game * 10000
    while True:
        if db.query(game_dict[_make_session_id.game]).filter(
                game_dict[_make_session_id.game].session_id == session_id).first():
            session_id = random.randint(1000, 9999) + (
                    db.query(game_dict[_make_session_id.game]).count() + 1) * 100000 + _make_session_id.game * 10000
        else:
            db_game = game_dict[_make_session_id.game](session_id=session_id, score=0,
                                                       student_id=_make_session_id.student_id,
                                                       name=_make_session_id.name)
            db.add(db_game)
            token_logging(db, _token_dec=_make_session_id)
            db.commit()
            return session_id


def add_user_token(db, _add_user_token: UserRequest):
    user = db.query(User).filter(User.student_id == _add_user_token.student_id).first()
    if user:
        user.token += _add_user_token.token_to_add
        db.commit()
        token_logging(db, _token_add=_add_user_token)
        return {'remain_token': user.token}
    else:
        raise HTTPException(status_code=http.HTTPStatus.UNAUTHORIZED, detail="no such user")


def create_user(db, _create_user: UserRequest):
    user = db.query(User).filter(User.student_id == _create_user.student_id).first()
    if user:
        raise HTTPException(status_code=http.HTTPStatus.CONFLICT, detail="user already exists")
    else:
        db.add(User(student_id=_create_user.student_id, name=_create_user.name, token=0))
        db.commit()
        return {'message': 'user created'}


def check_access_token(_user_request: UserRequest):
    if _user_request.admin_password == admin_password:
        return True
    else:
        return False


def token_logging(db, _token_add: UserRequest = None, _token_dec: SessionID = None):
    if _token_add:
        db.add(TokenLog(student_id=_token_add.student_id, name=_token_add.name,
                        token_delta=_token_add.token_to_add))
    elif _token_dec:
        db.add(TokenLog(student_id=_token_dec.student_id, name=_token_dec.name,
                        token_delta=-1))
    db.commit()
