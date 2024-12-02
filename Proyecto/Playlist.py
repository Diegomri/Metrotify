

class Playlist:

    def __init__(self, id, name, description, creator, tracks):
        self.id = id
        self.name = name
        self.description = description
        self.creator = creator
        self.tracks = tracks
        self.tracklist = []
        self.creatorName = ""
        self.likes = 0
        self.streams = 0

    def show_attr(self):
        return f"\n    Nombre: {self.name}\n    Descripcion: {self.description}\n    Creador: {self.creatorName}\n        Tracklist:\n  {self.tracklist}"