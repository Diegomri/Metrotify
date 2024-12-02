from User import User

class Listener(User):
    def __init__(self, id, name, email, username, type_):
        super().__init__(id, name, email, username, type_)
        self.Album_likes = []
        self.Song_likes = []
        self.playlistLikes = []
        self.playlists = []
        self.artistaslikes = []
    
    def Playlists(self):
        cadena = "  "
        for i, playlist in enumerate(self.playlists):
            cadena +=  f"\n        {i+1}.  {playlist.name}\n"
        return cadena

    def show_attr(self):
        return super().show_attr() + f"    Álbumes gustadoss: {self.Album_likes}\n    Canciones gustadas: {self.Song_likes}\n    Playlists: {self.Playlists()}"