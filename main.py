import uvicorn, os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.middleware import Middleware


from api.endpoints import student_router, user_router
from api.db.mongo_service import db_mongo



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

app.add_event_handler("startup", db_mongo.connect_to_mongo)
app.add_event_handler("shutdown", db_mongo.close_mongo_connection)



try:
    app.mount("/static", StaticFiles(directory='static'), name="static")
except:
    os.mkdir("static")

def configure() -> None:
    app.include_router(student_router.router)
    app.include_router(user_router.router)

configure()

if __name__ == '__main__':
    uvicorn.run(app, host="localhost",port=5002)  
    #uvicorn.run("api:app", host="localhost", port=5002, reload=True)