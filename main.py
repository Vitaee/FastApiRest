from starlette import middleware
from starlette.routing import Host
import uvicorn
from api import app
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.middleware import Middleware


middleware = [Middleware(CORSMiddleware,allow_origins=['*'], allow_credentials=True, 
                allow_methods=['*'], allow_headers=['*'])]

api = FastAPI(
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redocs",
    title="FastApi with Mongodb",
    description="Learning more about FastApi",
    version="1.0",middleware=middleware
)

api.mount("/static", StaticFiles(directory='static'), name="static")

def configure() -> None:
    api.include_router(app.router)

configure()

if __name__ == '__main__':
    uvicorn.run(api, host="localhost",port=5002)  
    #uvicorn.run("api:app", host="localhost", port=5002, reload=True)