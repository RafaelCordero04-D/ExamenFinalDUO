from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional


class jugadorBase(SQLModel):
    name: str | None = Field(description= "Jugador name")
    Ncamisa: int | None = Field(description = "Numero de camisa" )
    Fecha: int | None = Field(description= "Fecha de nacimiento")
    estado: str | None = Field(description= "Estado del jugador")
    alive : bool | None = Field(description = "True = active, False= deleted", default = True)
    img: Optional[str] = Field(default = None, description="Jugador Image")

class SpiderMan(JugadorBase, table=True):
    id: int | None = Field(default = None, primary_key=True)
    universe_id:int =Field(foreign_key = "universe.id")
    Universe: universe = Relationship(back_populates="spiderMans")