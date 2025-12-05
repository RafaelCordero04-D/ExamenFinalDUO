from db import SessionDep
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import APIRouter, HTTPException, Form, File, UploadFile, Request
from models import SpiderMan, spiderManCreate, universe, spiderManUpdate
from sqlmodel import select
from fastapi.templating import Jinja2Templates
from typing import Optional
import time

router = APIRouter

Templates = Jinja2Templates(directory="TemplatesHTML")

@router.get("/newSpider", response_class=HTMLResponse)
async def show_create(request: Request, universe_id: int):
    return Templates.TemplateResponse("new_spiderMan.html", {"request": request, "universe_id": universe_id})

#CREAR SPIDER-MAN
@router.post("/", response_model=SpiderMan, status_code=201)
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
        print(f"Uploading image: {img.filename}")
        try:
            # Append timestamp to filename to avoid duplicates
            timestamp = int(time.time())
            file_extension = img.filename.split('.')[-1] if '.' in img.filename else 'jpg'
            new_filename = f"{img.filename.split('.')[0]}_{timestamp}.{file_extension}"
            img.filename = new_filename
            
            img_url = await upload_to_bucket(img)
            print(f"Image uploaded: {img_url}")
        except Exception as e:
            print(f"Error uploading image: {e}")
            # If upload fails (e.g. duplicate or other error), we log it but don't stop the DB save.
            pass
            
    try:
        new_spider = spiderManCreate(name=name, alias=alias,skills=skills, alive=is_alive, img=img_url, universe_id=universe_id)
        print(f"Creating SpiderMan object: {new_spider}")

        spiderMan = SpiderMan.model_validate(new_spider)
        session.add(spiderMan)
        await session.commit()
        await session.refresh(spiderMan)
        print(f"SpiderMan saved with ID: {spiderMan.id}")
    except Exception as e:
        print(f"Error DB: {e}")
        raise HTTPException(status_code=400, detail=f"Error al guardar datos: {str(e)}")
    return RedirectResponse(url=f"/SpiderMans/{spiderMan.id}", status_code=302)