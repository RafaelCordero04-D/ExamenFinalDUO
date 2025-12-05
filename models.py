from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional




class historialEBase(SQLModel): 
    rival: str | None = Field(description= "rival") 
    Fecha: int | None = Field(description = "Fecha del Partido" ) 
    GolesR: str | None = Field(description= "Goles Rival") 
    GolesA: str | None = Field(description= "Goles Mi equipo")

class historialE(historialEBase, table=True)
    id: int | None = Field(default = None, primary_key=True)
    universe_id:int =Field(foreign_key = "universe.id") 
    Universe: universe = Relationship(back_populates="spiderMans")

class historialECreate(historialEBase):
    universe_id:int = Field(foreign_key = "universe.id")
    img: Optional[str] = None

class historialEUpdate(historialEBase):
    pass


class historialJBase(SQLModel):
    minutoE: str | None = Field(description= "minuto de Entrada del Jugador") 
    goles: int | None = Field(description = "goles del jugador" ) 
    targetas: str | None = Field(description= "targetas al jugador") 

class historialJ(historialJBase, table=True)
    id: int | None = Field(default = None, primary_key=True)
    jugador: list["Jugador"] = Relationship(back_populates="HistorialJ")

class historialJCreate(historialJBase):
    pass


class historialJUpdate(historialJBase):
    pass

class jugadorBase(SQLModel):
    name: str | None = Field(description= "Jugador name")
    Ncamisa: int | None = Field(description = "Numero de camisa" )
    Fecha: int | None = Field(description= "Fecha de nacimiento")
    estado: str | None = Field(description= "Estado del jugador")
    alive : bool | None = Field(description = "True = active, False= deleted", default = True)
    nacio: str | None = Field(description = "nacionalidad del Jugador")
    altura: float | None = Field(description = "altura del jugador")
    pieD: str | None = Field(description = "Pie dominante")
    posicion: str | None = Field(description = "Posicion o rol del jugador")
    img: Optional[str] = Field(default = None, description="Jugador Image")

class Jugador(jugadorBase, table=True):
    id: int | None = Field(default = None, primary_key=True)
    historialJugador_id:int =Field(foreign_key = "historialJ.id") 
    HistorialJ: historialJ = Relationship(back_populates="jugadores")

class jugadorCreate(jugadorBase):
    universe_id:int = Field(foreign_key = "universe.id")
    img: Optional[str] = None

class jugadorUpdate(jugadorBase):
    pass