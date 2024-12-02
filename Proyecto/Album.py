

class Album:

    def __init__(self, id, name, description, cover, date, genre, artist, tracklist):
        self.id = id
        self.name = name
        self.description = description
        self.cover = cover
        self.date = date
        self.genre = genre
        self.artist = artist
        self.creator = ""
        self.tracklist = tracklist
        self.tracks = []
        self.likes = 0
        self.streams = 0

    def canciones(self, song):
        self.tracks.append(song)

    def show_tracklist(self):
        cadena = "  Tracklist:\n"
        for i, song in enumerate(self.tracks):
            cadena +=  f"                {i+1}.  Canción{song.show_attr()}\n"
        return cadena

    def show_attr(self):
        return f"\n    Nombre: {self.name}\n    Descripcion: {self.description} \n    Portada: {self.cover}\n    Genero: {self.genre}\n    Creador: {self.creator}\n    Fecha de publicacion: {self.date}\n {self.show_tracklist()}"

    