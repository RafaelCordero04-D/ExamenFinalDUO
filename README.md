# ExamenFinalDUO

Rafa ves esto?
 si 
ahh oka 

 como vas danny? 

danny voy a crear otro modelo, que es historial para asociar los minutos y eso me dices que vas hacer 


 Rafa ya tengo el modelo del partido, como lo pide la parte de atras de la hoja, pero entonces esto usa 3 modelos no? serian jugador, equipo y partido.
 la cosa esque hago git pull y nose si tu ves los cambios Rafael: No todavia no veo los cambios en el repo 
 
vale, elproblema es que son cuatro, jugadores, partido, historial del jugador y hisorial del equipo(en si sus partidos), puedes revisarlo atras de la hoja 

Rafael: No todavia no veo los cambios en el repo 
 
vale, elproblema es que son cuatro, jugadores, partido, historial del jugador y hisorial del equipo(en si sus partidos), puedes revisarlo atras de la hoja 

 Rafa me sale un error todo hpta raro asi que te lo mando por aca lo que me pediste
class Equipo(EquipoBase, table=True):
    id: int | None = Field(default = None, primary_key=True)
    universe_id:int =Field(foreign_key = "universe.id")
    Universe: universe = Relationship(back_populates="spiderMans")

    peliculas: list["Pelicula"] = Relationship(back_populates = "spiderMans", link_model = SpiderManPeliculaLink)
    
class PartidoBase(SQLModel):
    rival: str | None = Field(description= "rival")
    Fecha: int | None = Field(description = "Fecha del Partido" )
    GolesR: str | None = Field(description= "Goles Rival")
    GolesA: str | None = Field(description= "Goles Mi equipo")

class Partido(PartidoBase, table=True):
    id: int | None = Field(default = None, primary_key=True)
    universe_id:int =Field(foreign_key = "universe.id") 
    Universe: universe = Relationship(back_populates="spiderMans")

    peliculas: list["Pelicula"] = Relationship(back_populates = "spiderMans", link_model = SpiderManPeliculaLink)


