











class Palabra:
    # defino las variables del constructor
    def __init__(self, palabra_original, traduccion, categoria, aprendida=False):
        self.palabra_original = palabra_original  # palabra en el idioma original
        self.traduccion = traduccion  # traducción de la palabra
        self.categoria = categoria  # categoría a la que pertenece
        self.aprendida = aprendida  # estado de aprendizaje (True/False). La inicializo en False porque no considero que esté aprendida

    # función que cambia el estado de aprendida a True, indicando que la palabra ha sido aprendida
    def marcar_como_aprendida(self):
        self.aprendida = True

    # función que muestra los datos de una palabra
    def mostrar_datos_palabra(self):
        return f"{self.palabra_original} - {self.traduccion} ({'Aprendida' if self.aprendida else 'No aprendida'})"


class Usuario:
    # defino las variables del constructor
    def __init__(self, nombre):
        self.nombre = nombre  # nombre del usuario
        self.vocabulario = []  # lista de palabras que el usuario ha añadido para aprender

    # función que me permite agregar a la lista del vocabulario una palabra (instancia de la clase Palabra)
    def agregar_palabra(self, palabra):
        self.vocabulario.append(palabra)

    # función que lista las palabras de la lista vocabulario
    def listar_vocabulario(self):
        for palabra in self.vocabulario:
            print(palabra.mostrar_datos_palabra())

    # función que muestra solo las palabras que están ya aprendidas
    def palabras_aprendidas(self):
        return [palabra for palabra in self.vocabulario if palabra.aprendida]  # devuelve una lista filtrada


class Vocabulario:
    # defino las variables del constructor
    def __init__(self):
        self.lista_palabras = []  # lista de palabras

    # función que me permite añadir una nueva palabra a la lista de vocabulario (instancia de Palabra)
    def agregar_palabra(self, palabra_agregar, traduccion, categoria):
        palabra_nueva = Palabra(palabra_agregar, traduccion, categoria)  # creo la nueva palabra como instancia de la clase Palabra
        self.lista_palabras.append(palabra_nueva)  # añado la palabra a la lista

    # función que muestra una lista de vocabulario
    def listar_palabras(self):
        for cursor in self.lista_palabras:  # recorro la lista lista_palabras y las almaceno en cursor
            print(cursor.mostrar_datos_palabra())  # puedo utilizar la función mostrar_datos_palabra() porque tiene una instancia de la clase Palabra (concedida en la función anterior)

    # función que permite al usuario practicar el vocabulario
    def practicar_vocabulario(self):
        import random  # importo la librería random
        if self.lista_palabras:  # si no está vacía la lista
            palabra_random = random.choice(self.lista_palabras)  # muestro una palabra random de la lista
            respuesta = input(f"¿Cuál es la traducción de '{palabra_random.palabra_original}'? ")  # obtengo la respuesta del usuario
            # {palabra_random.palabra_original} --> obtengo el valor de la palabra en el idioma que el usuario está tratando de aprender
            if respuesta.lower() == palabra_random.traduccion.lower():  # compruebo que coinciden, poniéndolas en minúsculas
                print("¡CORRECTO!")
                palabra_random.marcar_como_aprendida()  # si acierta, esa palabra pasa a ser aprendida (True)
            else:
                print(f"Incorrecto. La respuesta correcta es '{palabra_random.traduccion}'.")  # si falla se mantiene en False
                # {palabra_random.traduccion} --> obtengo la traducción de la palabra que se ha preguntado
        else:
            print("No hay palabras en el vocabulario para practicar.")














#función principal
def main():
    usuario = Usuario("Usuario")  # creo una instancia de Usuario
    vocabulario = Vocabulario()   # creo una instancia de Vocabulario

    while True:  # bucle infinito para mostrar el menú hasta que el usuario decida salir
        opcion = input("---- Menú Principal. Seleccione una opción: ---- \n 1. Agregar Palabra \n 2. Listar Vocabulario \n 3. Practicar Vocabulario \n 4. Salir")   
        
        if opcion not in ['1', '2', '3', '4']:  # valido la opción
            print("Opción no válida. Por favor, seleccione una opción del 1 al 4.")
            continue  # vuelve al menú si la opción no es válida

        match opcion:
            case "1":  # agregar palabra
                palabra = input("Ingrese la palabra en el idioma original: ")
                traduccion = input("Ingrese la traducción: ")
                categoria = input("Ingrese la categoría: ")
                vocabulario.agregar_palabra(palabra, traduccion, categoria)  # agrega la palabra al vocabulario
                print("Palabra agregada con éxito.")

            case "2":  # listar vocabulario
                print("Vocabulario:")
                vocabulario.listar_palabras()  # lista las palabras del vocabulario

            case "3":  # practicar vocabulario
                vocabulario.practicar_vocabulario()  # permite al usuario practicar el vocabulario

            case "4":  # salir
                print("¡Hasta luego!")
                break  # rompe el bucle para salir

            case _:  # opción no válida
                print("Opción no válida. Por favor, seleccione una opción del 1 al 4.")

main()