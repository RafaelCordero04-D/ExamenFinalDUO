from db import SessionDep
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import APIRouter, HTTPException, Form, File, UploadFile, Request
from models import Jugador, jugadorCreate, universe, jugadorUpdate
from sqlmodel import select
from fastapi.templating import Jinja2Templates
from typing import Optional
import time
import os 

router = APIRouter

Templates = Jinja2Templates(directory="TemplatesHTML")

UPLOAD_FOLDER = "static/images"

@router.get("/newJugador", response_class=HTMLResponse)
async def show_create(request: Request, universe_id: int): 
    return Templates.TemplateResponse("new_spiderMan.html", {"request": request, "universe_id": universe_id})

#CREAR Jugador
@router.post("/", response_model=Jugador, status_code=201)
async def create_SpiderMan(request:Request,
                           session: SessionDep,
                           name: str = Form(..., alias="name"),
                           alias:str = Form(..., alias="alias"),
                           skills:str = Form(..., alias="skills"),
                           alive_str:str = Form(..., alias="alive"),
                           universe_id: int = Form(..., alias="universe_id"),
                           img: Optional[UploadFile] = File(None)
                           ):

    print(f"Received data: name={name}, alias={alias}, universe_id={universe_id}, alive={alive_str}")
    
    is_alive = str(alive_str).lower() == "true"
    img_url = None
    
    if img and img.filename:
        print(f"Processing image: {img.filename}")
        try:
            
            timestamp = int(time.time())
           # archivo o 'jpg' por defecto
            file_extension = img.filename.split('.')[-1] if '.' in img.filename else 'jpg'
            
            safe_filename = f"{name.replace(' ', '_')}_{timestamp}.{file_extension}" 
            
            
            file_path = os.path.join(UPLOAD_FOLDER, safe_filename)
            
            
            content = await img.read()
            with open(file_path, "wb") as f:
                f.write(content)

           
            img_url = f"/{UPLOAD_FOLDER}/{safe_filename}"
            print(f"Image saved locally: {img_url}")
            
        except Exception as e:
            print(f"Error saving image locally: {e}")
            
            pass
            
    try:
        new_spider = jugadorCreate(name=name, alias=alias, skills=skills, alive=is_alive, img=img_url, universe_id=universe_id)
        # ... (Resto de tu lógica de guardado en DB) ...
        # ...
        jugador = Jugador.model_validate(new_spider)
        session.add(jugador)
        await session.commit()
        await session.refresh(jugador)
        # ...
        
    except Exception as e:
        print(f"Error DB: {e}")
        raise HTTPException(status_code=400, detail=f"Error al guardar datos: {str(e)}")
        
    return RedirectResponse(url=f"/Jugadores/{jugador.id}", status_code=302)