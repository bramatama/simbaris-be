from typing import Union

from fastapi import FastAPI
from app.api.routes import test_connection
from app.api.routes import school_routes
from app.api.routes import auth_routes

app = FastAPI()

app.include_router(test_connection.router, prefix="/api")
app.include_router(school_routes.router, prefix="/api")
app.include_router(auth_routes.router, prefix="/api")

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}