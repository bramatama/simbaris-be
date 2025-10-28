from typing import Union

from fastapi import FastAPI
from app.api.routes import test_connection
from app.api.routes import school_routes
from app.api.routes import auth_routes
from app.api.routes import user_routes
from app.api.routes import team_routes

app = FastAPI()

app.include_router(test_connection.router, prefix="/api")
app.include_router(school_routes.router, prefix="/api")
app.include_router(auth_routes.router, prefix="/api")
app.include_router(user_routes.router, prefix="/api/users")
app.include_router(team_routes.router, prefix="/api")

@app.get("/")
def read_root():
    return {"Hello": "World"}
