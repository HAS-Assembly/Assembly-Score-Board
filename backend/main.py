import datetime
import random
import time

from fastapi import FastAPI, WebSocket, Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from sqlalchemy.orm import Session

import crud
from crud import get_game1, get_game2, get_game3, add_game1, add_game2, add_game3
from fastapi import Depends
from fastapi.middleware.cors import CORSMiddleware
from models import Game1, Game2, Game3, ApiLog
from schema import UploadGame1, SessionID, Scores, UploadGame, UserRequest

from database import get_db

description = """
---
# 게임 점수 관련 API

각 게임에 맞는 점수를 관리하기 위한 API입니다. `POST` 요청을 사용하여 세션 ID 및 유저(학생)의 학번, 이름, 현재 점수를 업데이트할 수 있습니다. 
점수에 관련된 요청사항이 있을 경우 연락을 부탁드립니다. 해당 게임에 맞는 API 엔드포인트를 사용하여 요청해 주시기 바랍니다.

* Unity: Game1
* Python: Game2

---

# 세션 아이디 발급

기본 정보를 입력 함과 동시에 세션 아이디 반환

---

# 상위 10명

스코어 보드에 사용할 상위 10명의 점수를 가져옵니다.


---

위 내용을 참고하여 필요한 기능을 구현하고 요청해 주시기 바랍니다. 추가적인 도움이 필요하거나 다른 내용에 대해 알고 싶으시다면 <del>언제든지</del> 물어보세요!

---

"""

tags_metadata = [
        {
                'name'       : '게임 점수',
                'description': "게임 점수 추가 또는 업데이트",
        },
        {
                'name'       : '세션 아이디 발급',
                'description': "세션 아이디를 발급합니다.",
        },
        {
                'name'       : '상위 10명',
                'description': "상위 10명의 점수를 가져옵니다.",
        }
]

app = FastAPI(
        title="어셈블리 게임 점수 판 백엔드",
        description=description,
        version="V1",
        contact={
                "name" : "안호성",
                "url"  : "https://github.com/BetaTester772",
                "email": "hoseong8115.dev@gmail.com",
        },
        license_info={
                "name"      : "MIT",
                "identifier": "MIT",
        },
        # docs_url="/docs", redoc_url="/redoc",
        docs_url=None, redoc_url=None,
        openapi_tags=tags_metadata,
)

# middleware cors
app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
)


@app.get("/scores", tags=["상위 10명"])
def get_scores(request: Request, dev: int = 0, db: Session = Depends(get_db)):
    """
    :param dev(dev mode): 0 == False, 1 == True
    """
    # api_logging(db, endpoint="/scores", request=request, game=0, session_id=0, student_id=0, name="", )
    if dev == 0:
        game1 = get_game1(db).to_dict(orient='records')
        # game2 = get_game2(db).to_dict(orient='records')
        # game3 = get_game3(db).to_dict(orient='records')
    elif dev == 1:
        game1 = [
                {"id": 1, "student_id": 22121, "name": "안호성", "score": 100, "session_id": 1},
                {"id": 2, "student_id": 22121, "name": "안호성", "score": 300, "session_id": 2},
                {"id": 3, "student_id": 22121, "name": "안호성", "score": 500, "session_id": 3},
                {"id": 4, "student_id": 22121, "name": "안호성", "score": 700, "session_id": 4},
                {"id": 5, "student_id": 22121, "name": "안호성", "score": 1000, "session_id": 5},
                {"id"        : 6, "student_id": 22121, "name": "안호성", "score": random.randint(0, 1000),
                 "session_id": random.randint(6, 100)},
                {"id"        : 7, "student_id": 22121, "name": "안호성", "score": random.randint(0, 1000),
                 "session_id": random.randint(101, 200)},
                {"id"        : 8, "student_id": 22121, "name": "안호성", "score": random.randint(0, 1000),
                 "session_id": random.randint(201, 300)},
                {"id"        : 9, "student_id": 22121, "name": "안호성", "score": random.randint(0, 1000),
                 "session_id": random.randint(301, 400)},
                {"id"        : 10, "student_id": 22121, "name": "안호성", "score": random.randint(0, 1000),
                 "session_id": random.randint(401, 500)},
        ]
        game1.sort(key=lambda x: x['score'], reverse=True)
    else:
        raise ValueError('invalid dev value')

    return {"game1": game1}


@app.post("/55390bf270", status_code=204, tags=["게임 점수"])
def upload_game1(request: Request, _upload_game: UploadGame1, db: Session = Depends(get_db)):
    """
    :param request:
    :param _upload_game: {
        session_id: int - 제공된 세션 아디이(반드시 기존에 밝급된 값이어야 함)
        name: str - 학생 이름(기존에 등록된 이름이어야 함)
        student_id: int - 학번(기존에 등록된 학번이어야 함)
        score: int - 게임 점수
        difficulty: int - 게임 난이도(1-쉬움 또는 3-어려움)
    }
    :param db:
    :return:
    """
    api_logging(db, endpoint="/upload_game1", request=request, student_id=_upload_game.student_id,
                name=_upload_game.name, score=_upload_game.score, session_id=_upload_game.session_id, game=1)
    add_game1(db, _upload_game)
    return


@app.post("/upload_game2", status_code=204, tags=["게임 점수"])
def upload_game2(request: Request, _upload_game: UploadGame, db: Session = Depends(get_db)):
    api_logging(db, endpoint="/upload_game2", request=request, student_id=_upload_game.student_id,
                name=_upload_game.name, score=_upload_game.score, session_id=_upload_game.session_id, game=2)
    add_game2(db, _upload_game)
    return


@app.post("/upload_game3", status_code=204, tags=["게임 점수"])
def upload_game3(request: Request, _upload_game: UploadGame, db: Session = Depends(get_db)):
    api_logging(db, endpoint="/upload_game3", request=request, student_id=_upload_game.student_id,
                name=_upload_game.name, score=_upload_game.score, session_id=_upload_game.session_id, game=3)
    add_game3(db, _upload_game)
    return


@app.post("/session_id", tags=["세션 아이디 발급"])
def make_session_id(request: Request, _make_session_id: SessionID, db: Session = Depends(get_db)):
    session_id = crud.make_session_id(db, _make_session_id)
    api_logging(db, endpoint="/session_id", request=request, game=_make_session_id.game,
                student_id=_make_session_id.student_id,
                name=_make_session_id.name, session_id=session_id)
    return {'session_id': session_id}


def api_logging(db, endpoint, request, game, session_id, student_id, name, score=0):
    db.add(
            ApiLog(endpoint=endpoint, ip=request.client.host, game=game, student_id=student_id, name=name, score=score,
                   session_id=session_id))
    db.commit()


@app.post('/add_user_token')
def add_user_token(request: Request, _add_user_token: UserRequest, db: Session = Depends(get_db)):
    if not crud.check_access_token(_add_user_token):
        raise HTTPException(status_code=403, detail="invalid access token".format(_add_user_token.admin_password))
    api_logging(db, endpoint="/add_user_token", request=request, game=0, session_id=0,
                student_id=_add_user_token.student_id,
                name="", score=0)
    return crud.add_user_token(db, _add_user_token)


@app.post('/create_user')
def create_user(request: Request, _create_user: UserRequest, db: Session = Depends(get_db)):
    if not crud.check_access_token(_create_user):
        raise HTTPException(status_code=403, detail="invalid access token".format(_create_user.admin_password))
    api_logging(db, endpoint="/create_user", request=request, game=0, session_id=0, student_id=_create_user.student_id,
                name="", score=0)
    return crud.create_user(db, _create_user)


@app.get("/")
def index():
    return FileResponse("console/index.html")


app.mount("/_app", StaticFiles(directory="./console/_app"), name="static")


@app.get("/score_board")
def score_board():
    return FileResponse("board/index.html")


app.mount("/static", StaticFiles(directory="./board/static"), name="static")
