import uvicorn
from fastapi import FastAPI

from web import web_films

from api import api_films

app = FastAPI()
app.include_router(api_films.router)
app.include_router(web_films.router)


if __name__ == "__main__":

    uvicorn.run("main:app", host='0.0.0.0', reload=True, port=9500)
