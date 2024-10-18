import json
import os
import random

class Palabra:
    def __init__(self, palabra_original, traduccion, categoria, aprendida=False):
        self.palabra_original = palabra_original
        self.traduccion = traduccion
        self.categoria = categoria
        self.aprendida = aprendida

    def marcar_como_aprendida(self):
        self.aprendida = True

    def mostrar_datos_palabra(self):
        return f"{self.palabra_original} - {self.traduccion} ({'Aprendida' if self.aprendida else 'No aprendida'})"

class Usuario:
    def __init__(self, nombre):
        self.nombre = nombre
        self.vocabulario = []
        self.cargar_vocabulario()

    def cargar_vocabulario(self):
        try:
            if os.path.exists(f'{self.nombre}_vocabulario.json'):
                with open(f'{self.nombre}_vocabulario.json', 'r') as fichero_personal_usuario:
                    carga_datos = json.load(fichero_personal_usuario)
                    self.vocabulario = [Palabra(**palabra) for palabra in carga_datos]
            else:
                print("Usuario no registrado. Se va a crear un nuevo espacio para su práctica de vocabulario.")
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error al cargar el vocabulario: {e}")

    def guardar_vocabulario(self):
        try:
            with open(f'{self.nombre}_vocabulario.json', 'w') as f:
                json.dump([vars(palabra) for palabra in self.vocabulario], f, separators=(',', ':\n'))
        except IOError as e:
            print(f"Error al guardar el vocabulario: {e}")

    def agregar_palabra(self, palabra):
        self.vocabulario.append(palabra)
        self.guardar_vocabulario()

    def listar_vocabulario(self):
        for palabra in self.vocabulario:
            print(palabra.mostrar_datos_palabra())

    def palabras_aprendidas(self):
        return [palabra for palabra in self.vocabulario if palabra.aprendida]

class Vocabulario:
    def __init__(self):
        self.usuarios = {}  # Usamos un diccionario para almacenar instancias de Usuario con su nombre como clave
        self.todas_palabras_usuarios = []  # Lista para almacenar todas las palabras de todos los usuarios

    def agregar_usuario(self, usuario):
        self.usuarios[usuario.nombre] = usuario

    def agregar_palabra(self, palabra_agregar, traduccion, categoria, usuario):
        palabra_nueva = Palabra(palabra_agregar, traduccion, categoria)
        usuario.agregar_palabra(palabra_nueva)
        self.todas_palabras_usuarios.append(palabra_nueva)  # Agrega la palabra al vocabulario global

    def practicar_vocabulario(self, usuario):
        if usuario.vocabulario:
            palabra_random = random.choice(usuario.vocabulario)
            respuesta = input(f"¿Cuál es la traducción de '{palabra_random.palabra_original}'? ")
            if respuesta.lower() == palabra_random.traduccion.lower():
                print("¡CORRECTO!")
                palabra_random.marcar_como_aprendida()
                usuario.guardar_vocabulario()
            else:
                print(f"Incorrecto. La respuesta correcta es '{palabra_random.traduccion}'.")
        else:
            print("No hay palabras en el vocabulario para practicar.")

    def listar_vocabularios_todos(self):
        if not self.todas_palabras_usuarios:  # si no hay palabras globales
            print("No hay palabras en el vocabulario global.")
            return
        for cursor in self.todas_palabras_usuarios:
            print(cursor.mostrar_datos_palabra())

def main():
    vocabulario = Vocabulario()

    while True:
        nombre_usuario = input("Ingrese su nombre de usuario (o 'salir' para terminar): ")
        if nombre_usuario.lower() == 'salir':
            print("¡Hasta luego!")
            break

        # si el usuario ya existe, uso la instancia existente
        if nombre_usuario in vocabulario.usuarios:
            usuario = vocabulario.usuarios[nombre_usuario]
            print(f"Bienvenido de nuevo, {nombre_usuario}!")
        else:
            usuario = Usuario(nombre_usuario)
            vocabulario.agregar_usuario(usuario)

        while True:
            opcion = input(f"\n---- Menú Principal para {nombre_usuario}. Seleccione una opción: ---- \n 1. Agregar Palabra \n 2. Listar vocabulario de {nombre_usuario} \n 3. Practicar vocabulario de {nombre_usuario} \n 4. Mostrar un listado de todas las palabras del vocabulario (de todos los usuarios) \n 5. Cambiar usuario \n 6. Salir \n")   
            
            if opcion not in ['1', '2', '3', '4', '5', '6']:
                print("Opción no válida. Por favor, seleccione una opción del 1 al 6.")
                continue

            match opcion:
                case "1":
                    palabra = input("Ingrese la palabra en el idioma original: ")
                    traduccion = input("Ingrese la traducción: ")
                    categoria = input("Ingrese la categoría: ")
                    vocabulario.agregar_palabra(palabra, traduccion, categoria, usuario)
                    print("Palabra agregada con éxito.")

                case "2":
                    print(f"Vocabulario de {usuario.nombre}:")
                    usuario.listar_vocabulario()

                case "3":
                    vocabulario.practicar_vocabulario(usuario)

                case "4":
                    print("Listado de todas las palabras del vocabulario:")
                    vocabulario.listar_vocabularios_todos()

                case "5":
                    print("Cambiando de usuario...")
                    break  # sale del bucle interno (menú principal) para elegir otro usuario

                case "6":
                    print("Saliendo...")
                    return  # finalizo el programa

                case _:
                    print("Opción no válida. Por favor, seleccione una opción del 1 al 6.")

main()