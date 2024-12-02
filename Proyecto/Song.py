

class Song:

    def __init__(self, id, name, s_lenght, link):
        self.id = id
        self.name = name
        self.s_lenght = s_lenght
        self.link = link
        self.streams = 0
        self.likes = 0

    def show_attr(self):
        return f"\n        Nombre: {self.name}\n        Duracion: {self.s_lenght}\n        Link: {self.link}\n"
        