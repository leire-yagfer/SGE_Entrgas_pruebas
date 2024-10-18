import json
import os
import random
from collections import defaultdict

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
                json.dump([vars(palabra) for palabra in self.vocabulario], f, indent=3)  # Usamos indent=4 para mejorar la legibilidad
        except IOError as e:
            print(f"Error al guardar el vocabulario: {e}")

    def agregar_palabra(self, palabra):
        # Verificamos si la palabra ya existe en el vocabulario
        if any(p.palabra_original.lower() == palabra.palabra_original.lower() for p in self.vocabulario):
            print("La palabra ya existe en su vocabulario.")
            return  # Salimos si la palabra ya está
        else:
            self.vocabulario.append(palabra)
            self.guardar_vocabulario()

    def listar_vocabulario(self):
        if not self.vocabulario:  # Verificamos si el vocabulario está vacío
            print("Todavía no hay palabras en su vocabulario.")
        else:
            for palabra in self.vocabulario:
                print(palabra.mostrar_datos_palabra())

    def palabras_aprendidas(self):
        return [palabra for palabra in self.vocabulario if palabra.aprendida]

    def borrar_vocabulario(self):
        """Borra todo el vocabulario del usuario, dejando el archivo vacío."""
        self.vocabulario = []
        self.guardar_vocabulario()  # Guarda el estado vacío en el archivo
        print("Todo el vocabulario ha sido borrado.")

class Vocabulario:
    def __init__(self):
        self.usuarios = {}  # Usamos un diccionario para almacenar instancias de Usuario con su nombre como clave
        self.todas_palabras_usuarios = []  # Lista para almacenar todas las palabras de todos los usuarios
        self.palabras_unicas = set()  # Set para almacenar palabras únicas
        self.cargar_vocabulario_global()  # Cargar el vocabulario global al iniciar

    def cargar_vocabulario_global(self):
        """Carga el vocabulario global desde un archivo JSON si existe."""
        if os.path.exists('vocabulario_global.json'):
            with open('vocabulario_global.json', 'r') as f:
                self.todas_palabras_usuarios = json.load(f)
                # Añadir palabras únicas al set
                for palabra in self.todas_palabras_usuarios:
                    info_palabra = (palabra['palabra_original'].lower(), palabra['traduccion'], palabra['categoria'])
                    self.palabras_unicas.add(info_palabra)

    def guardar_vocabulario_global(self):
        """Guarda el vocabulario global en un archivo JSON."""
        try:
            with open('vocabulario_global.json', 'w') as f:
                json.dump(self.todas_palabras_usuarios, f, separators=(',', ':\n'))
        except IOError as e:
            print(f"Error al guardar el vocabulario global: {e}")

    def agregar_usuario(self, usuario):
        self.usuarios[usuario.nombre] = usuario

    def agregar_palabra(self, palabra_agregar, traduccion, categoria, usuario):
        # Usamos una tupla para almacenar la información de la palabra
        info_palabra = (palabra_agregar.lower(), traduccion, categoria)

        # Verificamos si la palabra ya está en el vocabulario del usuario
        if any(p.palabra_original.lower() == palabra_agregar.lower() for p in usuario.vocabulario):
            print("La palabra ya existe en el vocabulario del usuario. Introduzca una nueva.")
            return  # Salimos si la palabra ya está en el vocabulario del usuario
        
        # Crear nueva palabra
        palabra_nueva = Palabra(palabra_agregar, traduccion, categoria)
        usuario.agregar_palabra(palabra_nueva)  # Intentamos agregar la palabra al vocabulario del usuario
        
        # Agregar la palabra al vocabulario global sin el estado de aprendizaje
        if info_palabra not in self.palabras_unicas:
            self.todas_palabras_usuarios.append({
                'palabra_original': palabra_agregar,
                'traduccion': traduccion,
                'categoria': categoria
            })  # Agrega la información de la palabra al vocabulario global sin 'aprendida'
            self.palabras_unicas.add(info_palabra)  # Agrega la palabra al set de palabras únicas
            self.guardar_vocabulario_global()  # Guarda el vocabulario global actualizado
            
        print("Palabra agregada con éxito.")

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
            print("Todavía no hay ninguna palabra almacenada.")
            return  # salgo de la función

        palabras_mostradas = set()  # Usamos un set para almacenar las palabras originales que ya hemos mostrado
        for info in self.todas_palabras_usuarios:
            if info['palabra_original'] not in palabras_mostradas:  # Si no hemos mostrado esta palabra
                print(f"{info['palabra_original']} - {info['traduccion']} (Categoría: {info['categoria']})")
                palabras_mostradas.add(info['palabra_original'])  # Añadimos la palabra al set para evitar repeticiones

    def listar_vocabulario_por_categoria(self):
        if not self.todas_palabras_usuarios:
            print("No hay palabras almacenadas.")
            return

        # Agrupamos palabras por categoría
        vocabulario_por_categoria = defaultdict(list)
        for palabra in self.todas_palabras_usuarios:
            vocabulario_por_categoria[palabra['categoria']].append(palabra)

        # Ordenamos las categorías y las palabras en cada categoría
        for categoria in sorted(vocabulario_por_categoria.keys()):
            print(f"Categoría: {categoria}")
            for palabra in sorted(vocabulario_por_categoria[categoria], key=lambda x: x['palabra_original']):
                print(f"  {palabra['palabra_original']} - {palabra['traduccion']}")

    def copiar_vocabulario_global_a_usuario(self, usuario):
        """Copia palabras del vocabulario global al vocabulario del usuario si no existen ya."""
        for info in self.todas_palabras_usuarios:
            palabra_nueva = Palabra(info['palabra_original'], info['traduccion'], info['categoria'])
            if not any(p.palabra_original.lower() == palabra_nueva.palabra_original.lower() for p in usuario.vocabulario):
                usuario.agregar_palabra(palabra_nueva)
                print(f"Palabra '{palabra_nueva.palabra_original}' copiada al vocabulario de {usuario.nombre}.")

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
            opcion = input(f"\n---- Menú Principal para {nombre_usuario}. Seleccione una opción: ---- \n 1. Agregar Palabra \n 2. Listar vocabulario de {nombre_usuario} \n 3. Practicar vocabulario de {nombre_usuario} \n 4. Mostrar un listado de todas las palabras del vocabulario (de todos los usuarios) \n 5. Listar vocabulario global por categoría \n 6. Copiar vocabulario global a mi vocabulario \n 7. Borrar todo el vocabulario de {nombre_usuario} \n 8. Cambiar usuario \n 9. Salir \n")   
            
            if opcion not in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                print("Opción no válida. Por favor, seleccione una opción del 1 al 9.")
                continue

            match opcion:
                case "1":
                    palabra = input("Ingrese la palabra en el idioma original: ")
                    traduccion = input("Ingrese la traducción: ")
                    categoria = input("Ingrese la categoría: ")
                    vocabulario.agregar_palabra(palabra, traduccion, categoria, usuario)

                case "2":
                    print(f"Vocabulario de {usuario.nombre}:")
                    usuario.listar_vocabulario()

                case "3":
                    vocabulario.practicar_vocabulario(usuario)

                case "4":
                    print("Listado de todas las palabras del vocabulario:")
                    vocabulario.listar_vocabularios_todos()

                case "5":
                    print("Listado del vocabulario global por categoría:")
                    vocabulario.listar_vocabulario_por_categoria()

                case "6":
                    print("Copiando vocabulario global a mi vocabulario...")
                    vocabulario.copiar_vocabulario_global_a_usuario(usuario)

                case "7":
                    usuario.borrar_vocabulario()

                case "8":
                    print("Cambiando de usuario...")
                    break  # sale del bucle interno (menú principal) para elegir otro usuario

                case "9":
                    print("Saliendo...")
                    return  # finalizo el programa

                case _:
                    print("Opción no válida. Por favor, seleccione una opción del 1 al 9.")

main()