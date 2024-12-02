from User import User
from Listener import Listener
from Artist import Artist
from Playlist import Playlist
from Album import Album
from Song import Song
import pickle
import requests
import random

class App:

    def __init__(self):
        self.users = []
        self.listeners = []
        self.artists = []
        self.albums = []
        self.playlists = []
        self.songs = []
        self.SesionIniciada = False
        self.sesion = None

#Modulo 1
        
    def read_users(self):
        with open("users.pickle", "rb") as f:
            self.users = pickle.load(f)

    def read_albums(self):
        with open("albums.pickle", "rb") as f:
            self.albums = pickle.load(f)
    
    def read_playlists(self):
        with open("playlists.pickle", "rb") as f:
            self.playlists = pickle.load(f)
    
    def read_songs(self):
        with open("songs.pickle", "rb") as f:
            self.songs = pickle.load(f)

    def save_users(self):
        with open("users.pickle", "wb+") as f:
            pickle.dump(self.users, f)
    
    def save_albums(self):
        with open("albums.pickle", "wb+") as f:
            pickle.dump(self.albums, f)
    
    def save_playlists(self):
        with open("playlists.pickle", "wb+") as f:
            pickle.dump(self.playlists, f)
    
    def save_songs(self):
        with open("songs.pickle", "wb+") as f:
            pickle.dump(self.songs, f)

    def descargarAPIUsers(self):
        res = requests.request(
            "GET", "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/users.json").json()

        for user in res:
            if user["type"] == 'musician':
                artist = Artist(user['id'], user['name'], user['email'],
                        user['username'], user['type'])
                self.artists.append(artist)
                self.users.append(artist)
                
            else:
                listener = Listener(user['id'], user['name'], user['email'],
                        user['username'], user['type'])
                self.listeners.append(listener)
                self.users.append(listener)
                
    def descargarAPIAlbums(self):
        res = requests.request(
            "GET", "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/albums.json").json()

        for album in res:
            album = Album(album["id"], album['name'], album['description'],
                        album['cover'], album['published'], album["genre"], album["artist"], album["tracklist"])

            self.albums.append(album)

            for song in album.tracklist:
                song = Song(song["id"], song["name"], song["duration"], song["link"])
                album.canciones(song)
                self.songs.append(song) 

            for user in self.users:
                if album.artist == user.id:
                    album.creator += user.username
        
        self.save_albums()
        self.save_songs()

    def descargarAPIPlaylist(self):
        res = requests.request(
            "GET", "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/playlists.json").json()
        for playlist in res:
            playlist = Playlist(playlist["id"], playlist["name"], playlist["description"], playlist["creator"], playlist["tracks"])
            self.playlists.append(playlist)
        
            for song in playlist.tracks:
                for x in self.songs:
                    if x.id == song:
                        playlist.tracklist.append(x.name)
            
            for user in self.users:
                if playlist.creator == user.id:
                    playlist.creatorName += user.username
        
        self.save_playlists()
            
    def Generador_id(self, count):
        caracteres_id = list("abcdefghijklmnñopqrstuvwxyz0123456789")
        x = 0
        output = ""
        idExiste = False
        while x <= count:
            output += random.choice(caracteres_id)
            for user in self.users:
                if user.id ==  output:
                    idExiste = True
            for album in self.albums:
                if album.id == output:
                    idExiste = True
            for song in self.songs:
                if song.id ==  output:
                    idExiste = True
            for playlist in self.playlists:
                if playlist.id == output:
                    idExiste = True
            if idExiste == True:
                x = x
            else:
                x +=1
        return output
    
    def Validación(self, dato):
        perfilEncontrado = False
        for user in self.users:
            if dato == user.name or dato == user.email or dato == user.username:
                perfilEncontrado = True 
        if perfilEncontrado == True:
            return True
        else:
            return False

    def registro(self):
        id = ""
        caracteres_correo = "abcdefghijklmnñopqrstuvwxyz0123456789._@"
        id += self.Generador_id(8) + "-" + self.Generador_id(4) + "-" + self.Generador_id(4) + "-" + self.Generador_id(4) + "-" + self.Generador_id(12)

        Nombre = str(input("\n    Ingresa tu nombre completo: \n"))
        
        Username = str(input("\n    Ingresa tu nombre de usuario: \n"))
        self.Validación(Username)
        if self.Validación(Username) == True:
            print("\n  Ese nombre de usuario ya está en uso. Intente con otro.")
            return
        
        correo = str(input("\n    Ingresa tu correo: "))
        if "@" not in correo:
            print("\n Debe contener un arroba")
            return
        if "." not in correo:
            print("\n Debe contener un punto")
            return
        elif " " in correo:
            print("\n No se pemiten espacios.")
            return
        for letra in correo:
            if letra not in caracteres_correo:
                    print(f"\n El caracter {letra} no se permite.")
                    return
        self.Validación(correo)
        if self.Validación(correo) == True:
            print("\n  Ese correo ya está en uso. Intente con otro.")
            return

        tipo = input("\n    Que tipo de usuario eres?: \n  1. Músico\n  2. Escucha\n")
        if  tipo == '1':
            user = Artist(id, Nombre, correo, Username, "musician")
            self.users.append(user)
            self.artists.append(user)
            print("\n  Usuario registrado!")
            return self.users
        else:
            user = Listener(id,Nombre,correo,Username,"listener")
            self.users.append(user)
            self.listeners.append(user)
            print("\n  Usuario registrado!")
            self.save_users()
            return self.users
    
    def BuscarPerfiles(self):
        x = input("\n  Ingrese el nombre de usuario del perfil\n")
        perfilEncontrado = False
        for user in self.users:
            if x == user.username:
                perfilEncontrado = True 
                perfil = user
        if perfilEncontrado == False:
            print("\n  No se ha encontrado ese perfil")
        else:
            if perfil.type_ == "musician":
                for album in self.albums:
                    if perfil.albumes_creados == []:
                        perfil.albumes_creados.append(album)
                    else:
                        pass

                print(f"\n  Datos: \n    {perfil.show_attr()}")

                y = input("\n Desea darle like a este artista?\n  1. Si\n  2. No\n\n")
                if y == "1":
                    if perfil.username in self.sesion.artistaslikes:
                        print("\n Ya le has dado like a este artista. Deseas retirarlo?\n ")
                        y = input(("  1. Si\n  2. No\n"))
                        if y == "1":
                            perfil.likes -= 1
                            self.sesion.artistaslikes.remove(perfil.username)
                            print("\n  Like Eliminado")
                            self.save_users()
                            return
                        else:
                            pass
                    else:
                        perfil.likes =+ 1
                        self.sesion.artistaslikes.append(perfil.username)
                        print("\n  Like Agregado\n")
                        self.save_users()
                        return
                elif y == "2":
                    return
                else:
                    print("\n Dato invalido")
            else:
                for playlist in self.playlists:
                    if playlist.creator == perfil.id:
                        perfil.playlists = []
                        perfil.playlists.append(playlist)


                print(f"\n  Datos: \n    {perfil.show_attr()}")
    
    def CambiarInfo(self):
        
    
        while True:
            option2 = input("\n    Qué dato desea cambiar?\n  1. Nombre\n  2. Nombre de usuario\n  3. Correo electrónico\n  4. Salir\n")
            if option2 == "1":
                NewName = input("\n Ingrese su nuevo nombre.\n")
                self.sesion.name = NewName
                print("\nDatos Cambiados!\n")
            elif option2 == "2":
                NewUserName = input("\n Ingrese su nuevo nombre de usuario.\n")
                self.Validación(NewUserName)
                if self.Validación(NewUserName) == True:
                    print("\n  Ese nombre de usuario ya está en uso. Intente con otro.\n")
                    return
                else:
                    self.sesion.username = NewUserName
                    print("\nDatos Cambiados!\n")
            elif option2 == "3":
                caracteres_correo = "abcdefghijklmnñopqrstuvwxyz0123456789._@"
                NewEmail = input("\n Ingrese su nuevo correo.\n")
                if "@" not in NewEmail:
                    print("\n Debe contener un arroba")
                    return
                if "." not in NewEmail:
                        print("\n Debe contener un punto")
                        return
                elif " " in NewEmail:
                    print("\n No se pemiten espacios.")
                    return
                for letra in NewEmail:
                    if letra not in caracteres_correo:
                            print(f"\n El caracter {letra} no se permite.")
                            return
                self.Validación(NewEmail)
                if self.Validación(NewEmail) == True:
                    print("\n  Ese correo ya está en uso. Intente con otro.\n")
                    return
                else:
                    self.sesion.email = NewEmail
                    print("\nDatos Cambiados!\n")
            else:
                return

    def BorrarCuenta(self):
        option = input("\n    Seguro de querer borrar tu cuenta?\n  1. Si\n  2. No\n")
        if option == "1":
            self.users =[user for user in self.users if user != self.sesion]
            print("\n Datos Borrados!\n")
            self.SesionIniciada = False
            self.save_users()
            return 
        elif option == "2":
            return
        
    def LogIn(self):
        usuario = input("\n Ingrese el correo de su cuenta\n")
        perfilEncontrado = False
        for user in self.users:
            if usuario == user.email:
                perfilEncontrado = True 
                usuario = user
                self.SesionIniciada = True
                self.sesion = usuario
                print(f"\n Sesion iniciada")
                return self.sesion, self.SesionIniciada
        if perfilEncontrado == False:
            print("\n  No se ha encontrado ese perfil.")
            return

    def LogOut(self):
        self.SesionIniciada=False
        self.sesion = None
        print("\n Sesion cerrada.\n")

    def GestionPerfiles(self):
        while True: 
            if self.SesionIniciada == False:
                return
            else:
                try:
                    option = input('\n    Gestión de perfil\n  Qué desea hacer?\n  1. Buscar perfiles\n  2. Cambiar información personal de la cuenta\n  3. Cerrar Sesion \n  4. Borrar datos de la cuenta\n  5. Salir\n')
                    if option == "1":
                        self.BuscarPerfiles()
                    elif option == "2":
                        self.CambiarInfo()
                    elif option == "3":
                        self.LogOut()
                    elif option == "4":
                        self.BorrarCuenta()
                    elif option == "5":
                        self.save_users()
                        self.start()
                    else:
                        print("\n Dato Invalido")
                except:
                    print("\n Dato Invalido")

    def borrarTodo(self):
        with open('users.pickle', 'wb') as f:
            pickle.dump([], f)

        with open('albums.pickle', 'wb') as f:
            pickle.dump([], f)

        with open('playlists.pickle', 'wb') as f:
            pickle.dump([], f)

        with open('songs.pickle', 'wb') as f:
            pickle.dump([], f)
        
        self.read_albums()
        self.read_playlists()
        self.read_songs()
        self.read_users()

#Modulo 2
        
    def CrearTracklist(self, numero, ATracklist):
        ASong = {}
        count = 1
        while count <= numero:
            Sid = self.Generador_id(8) + "-" + self.Generador_id(4) + "-" + self.Generador_id(4) + "-" + self.Generador_id(4) + "-" + self.Generador_id(12)
            SName = input(f"\n   Ingrese nombre de la cancion {count}:\n ")
            SLenght = input(f"\n  Ingrese la duracion de la cancion {count}:\n")
            SLink = input(f"\n  Ingrese el link de la cancion {count}:\n")
            ASong["id"] = Sid
            ASong["name"]=SName
            ASong["lenght"]=SLenght
            ASong["link"]=SLink
            ATracklist.append(ASong)
            count += 1
        return ATracklist

    def CrearAlbum(self):
        if self.sesion.type_ == "listener":
            print("\n  Ese usuario no es artista, no puede crear álbumes.")
            return
        else:
            AId = self.Generador_id(8) + "-" + self.Generador_id(4) + "-" + self.Generador_id(4) + "-" + self.Generador_id(4) + "-" + self.Generador_id(12)
            AName = input("\n   Ingrese nombre del album:\n ")
            ADesc = input("\n  Ingrese la descripción del album:\n")
            ACover = input("\n  Ingrese el link de la portada del album:\n")
            ADate = input("\n  Ingrese la fecha de publicación del album:\n")
            AGenero = input("\n  Ingrese el género musical del album:\n")
            try:
                NCanciones = int(input("\n  Ingrese el número de canciones que tendrá el album:\n"))
                if NCanciones < 1:
                    print("\n  Un album debe contener al menos una cancion\n")
                    self.start()
            except:
                print("\n  Dato invalido\n")
            ATracklist = []
            self.CrearTracklist(NCanciones, ATracklist)
            album = Album(AId, AName, ADesc, ACover, ADate, AGenero, self.sesion.id, ATracklist)
            for song in album.tracklist:
                song = Song(song["id"], song["name"], song["lenght"], song["link"])
                album.canciones(song)
                self.songs.append(song)

            for user in self.users:
                if album.artist == user.id:
                    album.creator += user.username
            print(f"\n  Album creado con exito:\n{album.show_attr()}")
            self.albums.append(album)
            self.save_users()
            self.save_albums()
            self.save_songs()

    def PlaylistTracks(self, PTracks):

        while True:
            option = input("\n  1. Agregar canciones a la playlist. \n  2. Salir\n")
            if option == '1':
                cancion = input("\n  Introduzca el nombre de la cancion\n")
                cancionEncontrada = False
                for song in self.songs:
                    if cancion == song.name:
                        cancionEncontrada = True 
                        cancion = song
                        PTracks.append(cancion.id)
                        print("\n  Cancion añadida\n")
                        
                if cancionEncontrada == False:
                    print("\n  No se ha encontrado esa cancion")
            elif option == "2":
                if PTracks == []:
                    print("\n  La playlist debe contener al menos una cancion\n")
                else:
                    return PTracks
            else:
                print("\n  Dato invalido\n")                   

    def CrearPlaylist(self):
        if self.sesion.type_ == "musician":
            print("\n  Ese usuario es artista, no puede crear playlists.")
            return
        else:
            PId = self.Generador_id(8) + "-" + self.Generador_id(4) + "-" + self.Generador_id(4) + "-" + self.Generador_id(4) + "-" + self.Generador_id(12)
            PName = input("\n   Ingrese nombre de la playlist:\n ")
            PDesc = input("\n  Ingrese la descripción de la playlist:\n")
            PTracks = []
            self.PlaylistTracks(PTracks)
            playlist = Playlist(PId, PName, PDesc, self.sesion.id, PTracks)
            
            for song in playlist.tracks:
                for x in self.songs:
                    if x.id == song:
                        playlist.tracklist.append(x.name)
        
            for user in self.users:
                if playlist.creator == user.id:
                    playlist.creatorName += user.username
            print(f"\n  Playlist creada con exito:\n{playlist.show_attr()}")
            self.playlists.append(playlist)
            self.save_users()
            self.save_playlists()

    def BuscarAlbum(self, x):
        albumEncontrado = False
        for album in self.albums:
            if x == album.name:
                albumEncontrado = True 
                albumE = album
        if albumEncontrado == False:
            return False

        else:
            albumE.streams = albumE.streams + 1
            for user in self.users:
                if user.id == albumE.artist:
                    user.streams = user.streams + 1
            while True:
                print(albumE.show_attr())
                
                option = input("\n  Que desea hacer?\n  1. Darle like al album\n  2. Escuchar una cancion\n  3. Salir\n")
                if option == "1":
                    if albumE.name in self.sesion.Album_likes:
                        print("\n Ya le has dado like a este album. Deseas retirarlo?\n ")
                        y = input(("  1. Si\n  2. No\n"))
                        if y == "1":
                            albumE.likes -= 1
                            self.sesion.Album_likes.remove(albumE.name)
                            print("\n  Like Eliminado")
                        else:
                            pass
                    else:
                        albumE.likes =+ 1
                        self.sesion.Album_likes.append(albumE.name)
                        print("\n  Like Agregado\n")
                elif option == "2":
                    s = input("\n Introduce el nombre de la cancion que deseas escuchar\n")
                    CancionEncontrado = False
                    for song in albumE.tracks:
                        if s == song.name:
                            CancionEncontrado = True 
                            SongE = song
                    if CancionEncontrado == False:
                        print("\n  Esa cancion no se encuentra en este album.\n")
                    else:
                        print(f"\n  Link de la canción: {SongE.link}")
                        SongE.streams +=1
                        SLike = input("\n  Desea darle like?\n  1. Si\n  2. No\n")
                        if SLike =="1":
                            if SongE.name in self.sesion.Song_likes:
                                print("\n Ya le has dado like a esta cancion. Deseas retirarlo?\n ")
                                z = input(("  1. Si\n  2. No\n"))
                                if z == "1":
                                    SongE.likes -= 1
                                    self.sesion.Song_likes.remove(SongE.name)
                                    print("\n  Like eliminado\n")
                                else:
                                    pass
                            else:
                                SongE.likes =+ 1
                                self.sesion.Song_likes.append(SongE.name)
                                print("\n  Like agregado\n")
                        else:
                            pass
                elif option == "3":
                    
                    self.save_users()
                    self.save_albums()
                    self.save_songs()
                    self.start()
                else:
                    print("\n  Dato invalido\n")

    def BuscarCancion(self, x):
        CancionEncontrado = False
        for song in self.songs:
            if x == song.name:
                CancionEncontrado = True 
                SongE = song
        if CancionEncontrado == False:
            return False
        
        else:
            print(f"\n  Link de la canción: {SongE.link}")
            SongE.streams += 1
            for album in self.albums:
                for track in album.tracklist:
                    if SongE.id in track["id"]:
                        for user in self.users:
                            if user.id == album.artist:
                                user.streams = user.streams + 1
            SLike = input("\n  Desea darle like?\n  1. Si\n  2. No\n  3. Salir\n")
            if SLike =="1":
                if SongE.name in self.sesion.Song_likes:
                    print("\n Ya le has dado like a esta cancion. Deseas retirarlo?\n ")
                    z = input(("  1. Si\n  2. No\n"))
                    if z == "1":
                        SongE.likes -= 1
                        self.sesion.Song_likes.remove(SongE.name)
                        print("\n  Like eliminado\n")
                    else:
                        pass
                else:
                    SongE.likes =+ 1
                    self.sesion.Song_likes.append(SongE.name)
                    print("\n  Like agregado\n")
                    
            elif SLike == "2":
                self.save_users()
                self.save_songs()
                self.start()
            else:
                self.save_users()
                self.save_songs()
                self.start()

    def BuscarPlaylist(self, x):
        PLEncontrado = False
        for playlist in self.playlists:
            if x == playlist.name:
                PLEncontrado = True 
                playlistE = playlist
        if PLEncontrado == False:
            return False

        else:
            playlistE.streams = playlistE.streams + 1
            while True:
                print(playlistE.show_attr())
                option = input("\n  Que desea hacer?\n  1. Darle like a la playlist\n  2. Escuchar una cancion\n  3. Salir\n")
                if option == "1":
                    if playlistE.name in self.sesion.playlistLikes:
                        print("\n Ya le has dado like a esta playlist. Deseas retirarlo?\n ")
                        y = input(("  1. Si\n  2. No\n"))
                        if y == "1":
                            playlistE.likes -= 1
                            self.sesion.playlistLikes.remove(playlistE.name)
                            print("\n  Like Eliminado")
                        else:
                            pass
                    else:
                        playlistE.likes =+ 1
                        self.sesion.playlistLikes.append(playlistE.name)
                        print("\n  Like Agregado\n")
                elif option == "2":
                    s = input("\n Introduce el nombre de la cancion que deseas escuchar\n")
                    CancionEncontrado = False
                    for track in playlistE.tracklist:

                        if s == track:
                            for song in self.songs:
                                if  track == song.name:
                                    CancionEncontrado = True 
                                    SongE = song
                            if CancionEncontrado == False:
                                print("\n  Esa cancion no se encuentra en esta playlist.\n")
                            else:
                                print(f"\n  Link de la canción: {SongE.link}")
                                SongE.streams +=1
                                SLike = input("\n  Desea darle like?\n  1. Si\n  2. No\n")
                                if SLike =="1":
                                    if SongE.name in self.sesion.Song_likes:
                                        print("\n Ya le has dado like a esta cancion. Deseas retirarlo?\n ")
                                        z = input(("  1. Si\n  2. No\n"))
                                        if z == "1":
                                            SongE.likes -= 1
                                            self.sesion.Song_likes.remove(SongE.name)
                                            print("\n  Like eliminado\n")
                                        else:
                                            pass
                                    else:
                                        SongE.likes =+ 1
                                        self.sesion.Song_likes.append(SongE.name)
                                        print("\n  Like agregado\n")
                        else:
                            pass
                elif option == "3":
                    
                    self.save_users()
                    self.save_songs()
                    self.save_playlists()
                    self.start()
                else:
                    print("\n  Dato invalido\n")

    def BuscarArtista(self, x):
        perfilEncontrado = False
        for user in self.users:
            if x == user.username:
                perfilEncontrado = True 
                perfil = user
        if perfilEncontrado == False:
            return False
        else:
            if perfil.type_ == "musician":
                for album in self.albums:
                    if album.artist == perfil.id:
                        if perfil.albumes_creados == []:
                            perfil.albumes_creados.append(album)
                        else:
                            pass
                perfil.streams = perfil.streams + 1

                print(f"\n  Datos: \n    {perfil.show_attr()}")

                y = input("\n Que desea hacer?\n  1. Dar like al artista\n  2. Escuchar una cancion\n  3. Salir")
                if y == "1":
                    if perfil.name in self.sesion.artistaslikes:
                        print("\n Ya le has dado like a este artista. Deseas retirarlo?\n ")
                        y = input(("  1. Si\n  2. No\n"))
                        if y == "1":
                            perfil.likes -= 1
                            self.sesion.artistaslikes.remove(perfil.name)
                            print("\n  Like Eliminado")
                        else:
                            pass
                    else:
                        perfil.likes =+ 1
                        self.sesion.artistaslikes.append(perfil.name)
                        print("\n  Like Agregado\n")
                elif y == "2":
                    s = input("\n Introduce el nombre de la cancion que deseas escuchar\n")
                    CancionEncontrado = False
                    for album in perfil.albumes_creados:
                        for song in album.tracks:
                            if s == song.name:
                                CancionEncontrado = True 
                                SongE = song
                    if CancionEncontrado == False:
                        print("\n  No se ha encontrado esa cancion en el perfil de este artista\n")
                    else:
                        print(f"\n  Link de la canción: {SongE.link}")
                        SongE.streams +=1
                        SLike = input("\n  Desea darle like?\n  1. Si\n  2. No\n")
                        if SLike =="1":
                            if SongE.name in self.sesion.Song_likes:
                                print("\n Ya le has dado like a esta cancion. Deseas retirarlo?\n ")
                                z = input(("  1. Si\n  2. No\n"))
                                if z == "1":
                                    SongE.likes -= 1
                                    self.sesion.Song_likes.remove(SongE.name)
                                    print("\n  Like eliminado\n")
                                else:
                                    pass
                            else:
                                SongE.likes =+ 1
                                self.sesion.Song_likes.append(SongE.name)
                                print("\n  Like agregado\n")
                        else:
                            pass
                elif y == "3":
                    self.save_users()
                    self.save_songs()
                    self.start()
                else:
                    print("\n Dato invalido\n")

            else:
                return False

    def Buscador(self):
        x = input("\n  Ingrese el nombre de la cancion, playlist, album o artista\n")
        album = False
        cancion = False
        playlist = False
        artist = False

        if self.BuscarAlbum(x) == False:
            album = False
        else:
            album = True
        
        if self.BuscarCancion(x) == False:
            cancion = False
        else:
            cancion = True

        if self.BuscarPlaylist(x) == False:
            playlist = False
        else:
            playlist = True

        if self.BuscarArtista(x) == False:
            artist = False
        else:
            artist = True
        

        if album==True:
            self.BuscarAlbum(x)
        elif cancion == True:
            self.BuscarCancion(x)
        elif playlist == True:
            self.BuscarPlaylist(x)
        elif artist == True:
            self.BuscarArtista(x)
        elif album == False and cancion == False and playlist == False and artist == False:
            print("\n  No se ha encontrado ninguna coincidencia.\n")
                             
    def  GestionMusical(self):
        while True: 
            try:
                option = input('\n    Gestión musical\n  Qué desea hacer?\n  1. Crear un álbum\n  2. Crear una playlist\n  3. Buscador\n  4. Salir\n')
                if option == "1":
                    self.CrearAlbum()
                elif option == "2":
                    self.CrearPlaylist()
                elif option == "3": 
                    self.Buscador()
                elif option == "4":
                    self.save_albums()
                    self.save_playlists()
                    self.start()
                else:
                    print("\n Dato Invalido")
            except:
                print("\n Dato Invalido")

#El modulo 3 esta integrado en el resto

#Modulo 4
                
    def selection_sort(self, streams):
        for i in range(len(streams)):
            min_idx = i
            for j in range(i+1, len(streams)):
                if streams[min_idx] < streams[j]:
                    min_idx = j
            streams[i], streams[min_idx] = streams[min_idx], streams[i]
        
    def top5musicos(self):
        self.artists = []
        streams = []
        for user in self.users:
            if user.type_ == "musician":
                self.artists.append(user)
        
        for artist in self.artists:
            streams.append([artist.streams, artist.username])
        
        self.selection_sort(streams)
        print("\n    Top 5 artistas mas escuchados:")
        for i, x in enumerate(streams[:5]):
            print(f"{i+1}. {x[1]}: {x[0]}")
            
    def top5canciones(self):
        streams = []
        
        for song in self.songs:
            streams.append([song.streams, song.name])
        
        self.selection_sort(streams)
        print("\n    Top 5 canciones mas escuchadas:")
        for i, x in enumerate(streams[:5]):
            print(f"{i+1}. {x[1]}: {x[0]}")            
        
    def top5albumes(self):
        streams = []
        
        for album in self.albums:
            streams.append([album.streams, album.name])
        
        self.selection_sort(streams)
        print("\n    Top 5 albumes mas escuchados:")
        for i, x in enumerate(streams[:5]):
            print(f"{i+1}. {x[1]}: {x[0]}")    

    def top5playlist(self):
        streams = []
        
        for playlist in self.playlists:
            streams.append([playlist.streams, playlist.name])
        
        self.selection_sort(streams)
        print("\n    Top 5 playlists mas escuchadas:")
        for i, x in enumerate(streams[:5]):
            print(f"{i+1}. {x[1]}: {x[0]}") 

    def GestionEstadisticas(self):
        while True: 
            try:
                option = input('\n    Estadisticas\n  Qué desea hacer?\n  1. Top 5 musicos\n  2. Top 5 canciones\n  3. Top 5 albumes\n  4. Top 5 playlists\n  5. Salir\n')
                if option == "1":
                    self.top5musicos()
                elif option == "2":
                    self.top5canciones()
                elif option == "3": 
                    self.top5albumes()
                elif option == "4":
                    self.top5playlist()
                elif option == "5":
                    break
                else:
                    print("\n Dato Invalido")
            except:
                print("\n Dato Invalido")

    def start(self):
        ApiDescargadas = False
        self.read_albums()
        self.read_playlists()
        self.read_songs()
        self.read_users()

        while True:
                if self.SesionIniciada == False:
                    option = input("\n  Bienvenido a Metrotify. Que deseas hacer? \n  0. Descargar datos de la API\n  1. Iniciar sesión\n  2. Registrar un nuevo usuario\n  3. Borrar todos los datos\n")    
                    if option == "0":
                        if ApiDescargadas == False:
                            self.descargarAPIUsers()
                            self.descargarAPIAlbums()
                            self.descargarAPIPlaylist()
                            print("\n Datos descargados!\n")
                            ApiDescargadas = True
                        else:
                            print("\n  Ya se ha descargado la API\n")
                    elif option == "1":
                        self.LogIn()
                    elif option == "2":
                        self.registro()
                    elif option == "3":
                        self.borrarTodo()
                        print("\n  Datos borrados")
                    else:
                        print("\n  Dato Invalido")
                
                else:
                    try:
                        print(f"\n    Bienvenido a Metrotify, {self.sesion.name}")
                        option2 = str(input("\n  Qué desea hacer?\n    1. Gestión de perfil\n    2. Gestión musical\n    3. Estadisticas\n"))
                        if option2 == "1":
                            self.GestionPerfiles()
                        elif option2 == "2":
                            self.GestionMusical()
                        elif option2 == "3":
                            self.GestionEstadisticas()
                        else:
                            print("\n  Dato invalido\n")
                    except:
                        print("\n  Dato Invalido")