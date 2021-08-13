import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.middleware import Middleware


from api.endpoints import student_router
from api.db.mongo_db_utils import connect_to_mongo , close_mongo_connection



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
    openapi_tags=[ {"name":"Students", "description":"CRUD operations with students."} ]
)

app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)



app.mount("/static", StaticFiles(directory='static'), name="static")

def configure() -> None:
    app.include_router(student_router.router)

configure()

if __name__ == '__main__':
    uvicorn.run(app, host="localhost",port=5002)  
    #uvicorn.run("api:app", host="localhost", port=5002, reload=True)