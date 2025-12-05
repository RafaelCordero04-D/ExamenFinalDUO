from fastapi import APIRouter, Depends, HTTPException, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse
from sqlmodel import Session, select
from pathlib import Path
from fastapi.templating import Jinja2Templates

from ..database import get_session
from ..models import PartidoHistorialBase, AlbumCreate, AlbumRead, Artist
from ..utils import upload_image

# Configure templates
templates = Jinja2Templates(directory=str(Path(__file__).parent.parent / "templates"))

router = APIRouter(
    prefix="/Equipos",
    tags=["Equipos"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_class=HTMLResponse)
def read_albums(request: Request, session: Session = Depends(get_session)):
    albums = session.exec(select(Album)).all()
    return templates.TemplateResponse("albums/album_list.html", {"request": request, "albums": albums})

@router.get("/create", response_class=HTMLResponse)
def create_album_form(request: Request, session: Session = Depends(get_session)):
    artists = session.exec(select(Artist)).all()
    return templates.TemplateResponse("albums/album_create.html", {"request": request, "artists": artists})

@router.post("/create", response_class=HTMLResponse)
async def create_album(
    request: Request,
    Rival: str = Form(...),
    year: int = Form(...),
    artist_id: int = Form(...),
    file: UploadFile = File(None),
    session: Session = Depends(get_session)
):
    image_url = await upload_image(file, bucket_name="album_covers")
    album_data = AlbumCreate(name=name, year=year, artist_id=artist_id)
    db_album = Album.model_validate(album_data)
    db_album.image_url = image_url
    
    session.add(db_album)
    session.commit()
    session.refresh(db_album)

    return templates.TemplateResponse("albums/album_detail.html", {"request": request, "album": db_album})

@router.get("/{album_id}", response_class=HTMLResponse)
def read_album(album_id: int, request: Request, session: Session = Depends(get_session)):
    album = session.get(Album, album_id)
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")
    return templates.TemplateResponse("albums/album_detail.html", {"request": request, "album": album})



@router.post("/{album_id}/delete", response_class=HTMLResponse)
def delete_album(album_id: int, request: Request, session: Session = Depends(get_session)):
    album = session.get(Album, album_id)
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")
    
    session.delete(album)
    session.commit()
    
    return read_albums(request, session)
  
