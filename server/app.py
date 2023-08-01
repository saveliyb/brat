from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
import uvicorn
import os
from sqlalchemy.orm import Session
import pydantic_models
from config import start
import CRUD.victim
from database import get_session



app = FastAPI()


@app.on_event("startup")
async def startup_event():
    # set environ variables
    start()


@app.get("/victim/signUP")
async def victim_signUP(pdm_victim: pydantic_models.RegisterVictim, session: Session = Depends(get_session)):
    try:
        victim = CRUD.victim.register_victim(db=session, pdm_victim=pdm_victim)
        CRUD.victim.set_login_date(db=session, pdm_victim=victim)
        return victim.victim_hash_id
    except Exception as _ex:
        return JSONResponse(content={"message": "an unexpected error occurred on the server"}, status_code=500)


@app.get("/victim/update_data")
async def victim_update_data(pdm_victim: pydantic_models.UpdateDataVictim, session: Session = Depends(get_session)):
    try:
        CRUD.victim.update_data_victim(db=session, pdm_victim=pdm_victim)
        CRUD.victim.set_login_date(db=session, pdm_victim=pdm_victim)
        return "ok"
    except Exception as _ex:
        return JSONResponse(content={"message": "an unexpected error occurred on the server"}, status_code=500)


@app.get("/victim/login")
async def login(pdm_victim: pydantic_models.LoginVictim, session: Session = Depends(get_session)):
    try:
        CRUD.victim.set_login_date(db=session, pdm_victim=pdm_victim)
        return "ok"
    except Exception as _ex:
        return JSONResponse(content={"message": "an unexpected error occurred on the server"}, status_code=500)


if __name__ == '__main__':
    # start server with uvicorn
    uvicorn.run(f"{__name__}:app", host="127.0.0.1", port=8000)