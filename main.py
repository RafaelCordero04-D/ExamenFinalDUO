from fastapi import FastAPI, UploadFile, File, Form, Request, HTTPException
from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

import jugador

from db import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables(app)
    yield
app = FastAPI(lifespan= lifespan, title="Spiderman API")

app.mount("/TemplatesHTML", StaticFiles(directory="TemplatesHTML"), name="TemplatesHTML")
app.include_router(jugador.router, tags=["SpiderMan"], prefix="/SpiderMans")

app.mount("/estilos", StaticFiles(directory="estilos"), name="estilos")

Templates = Jinja2Templates(directory="TemplatesHTML")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return Templates.TemplateResponse("index.html", {"request": request})

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get("/nombre/{name}")
async def say_yourName(name: str):
    return {"presentation": f"Mi nombre es {name}"}