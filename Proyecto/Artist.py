from User import User

class Artist(User):
    def __init__(self, id, name, email, username, type_):
        super().__init__(id, name, email, username, type_)
        self.albumes_creados = []
        self.likes = 0
        self.Album_likes = []
        self.Song_likes = []
        self.playlistLikes = []
        self.artistaslikes = []
        self.streams = 0



    def Albumes(self):
        cadena = "  "
        for i, album in enumerate(self.albumes_creados):
            cadena +=  f"        {i+1}.  Album{album.show_attr()}\n"
        return cadena
    
    def show_attr(self):
        return super().show_attr() + f"    Albumes Creados:\n  {self.Albumes()}"