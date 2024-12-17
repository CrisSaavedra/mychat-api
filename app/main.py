from fastapi import FastAPI
from routers.app import router
from routers.user import UserRouter


app = FastAPI()

app.include_router(router, prefix="/v1" )