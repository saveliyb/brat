from fastapi import FastAPI
import uvicorn
import os
from dotenv import load_dotenv
# TODO come up with a short name for pydantic_models
import pydantic_models

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    # set environ variables
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)


@app.get("/")
async def index():
    return {"Hello": "World"}


@app.get("/env")
async def env():
    # TODO NOT FOR PRODUCTION
    return os.environ


@app.get("/victim_signUP")
async def victim_sign_UP(victim: pydantic_models.RegisterVictim) -> str:
    # TODO CRUD for victim registration
    victim = ""
    return victim.unique_number



if __name__ == '__main__':
    # start server with uvicorn
    uvicorn.run(f"{__name__}:app", host="127.0.0.1", port=8000)