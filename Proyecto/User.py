

class User:

    def __init__(self, id, name, email, username, type_):
        self.name = name
        self.id = id
        self.email = email
        self.username = username
        self.type_ = type_

    def show_attr(self):
        return f"\n    Nombre: {self.name}\n    Correo: {self.email} \n    Usuario: {self.username}\n"
        