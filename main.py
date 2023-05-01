import uvicorn, os, argparse, asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.middleware import Middleware

from src.modules.student.studentRoutes import router as student_router
from src.modules.user.userRoutes import router as user_router
from src.config.mongo_service import db_mongo
from src.utils.env_service import env_service


middleware = [Middleware(CORSMiddleware,allow_origins=['*'], allow_credentials=True, 
                allow_methods=['*'], allow_headers=['*'])]

app = FastAPI(
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redocs",
    title="FastApi with Mongodb",
    description="Learning more about FastApi",
    version="1.0",middleware=middleware,
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    contact={
        "name": "Can İlgu",
        "url":"http://github.com/Vitaee",
        "email": "canilguu@gmail.com",
    },
    openapi_tags=[ {"name":"Students", "description":"CRUD operations with students."},
                    {"name":"Users","description":"User Authentication"} ]
)

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("--env", type=str, required=False, choices=["test", "dev", "prod"], default="test")
args = arg_parser.parse_args()

if args.env == "test":
    app.include_router(student_router)
    app.include_router(user_router)
    env_service.load_env(args.env)
    #asyncio.run(db_mongo.connect_to_mongo())


@app.on_event("startup")
async def startup_event():
    configure()
    env_service.load_env(args.env)
    await db_mongo.connect_to_mongo()
    
app.add_event_handler("shutdown", db_mongo.close_mongo_connection)


try:
    app.mount("/static", StaticFiles(directory='static'), name="static")
except:
    os.mkdir("static")

def configure() -> None:
    app.include_router(student_router)
    app.include_router(user_router)


if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=5002, reload=True)