# Importamos los módulos necesarios
import csv                          # Para leer archivos CSV
from datetime import timedelta      # Para convertir milisegundos a formato HH:MM:SS
import re                           # Para trabajar con expresiones regulares

# Definimos la ruta del archivo CSV de trabajo
ARCHIVO = "C:/Users/anchi/OneDrive/Escritorio/Facultad/3ro/automatas y gramaticas/tp4/TrabajoIntegrador/datos_spotify.csv"

def mostrar_albumes():
    print("\n--- Mostrar álbumes de un artista ---")

    # Función interna para cargar los datos del CSV como una lista de diccionarios
    def cargar_datos():
        # Abrimos el archivo en modo lectura, con codificación UTF-8
        with open(ARCHIVO, newline='', encoding='utf-8') as f:
            # Retornamos una lista de filas como diccionarios
            return list(csv.DictReader(f))

    # Función que convierte duración en milisegundos a formato HH:MM:SS
    def ms_a_hhmmss(ms):
        return str(timedelta(milliseconds=int(ms)))  # timedelta hace la conversión automáticamente

    # Cargamos todos los datos del archivo
    datos = cargar_datos()

    # Normalizamos las claves de cada fila del archivo a minúsculas para evitar errores de mayúsculas/minúsculas
    datos = [{k.lower(): v for k, v in fila.items() if k is not None} for fila in datos]

    # Solicitamos al usuario el nombre del artista a buscar
    artista_input = input("Ingrese el nombre del artista: ").strip()

    # Creamos una expresión regular para buscar coincidencias sin distinguir mayúsculas o minúsculas
    patron_artista = re.compile(re.escape(artista_input), re.IGNORECASE)

    # Filtramos las filas donde el campo 'artist' coincida parcial o totalmente con la entrada del usuario
    canciones_artista = [
        fila for fila in datos
        if patron_artista.search(str(fila.get('artist') or ''))  # str(...) garantiza que no falle si hay None
    ]

    # Si no se encontraron canciones del artista ingresado, lo informamos
    if not canciones_artista:
        print("No se encontraron canciones para ese artista.")
        return

    # Creamos un diccionario donde agruparemos las canciones por álbum
    albumes = {}

    # Recorremos todas las canciones del artista encontradas
    for cancion in canciones_artista:
        # Obtenemos el nombre del álbum (si está vacío o None, se coloca 'Desconocido')
        nombre_album = str(cancion.get('album') or 'Desconocido')

        # Intentamos obtener la duración de la canción en milisegundos
        try:
            duracion_ms = int(float(cancion.get('duration_ms') or 0))  # Si está vacío o mal, usamos 0
        except ValueError:
            continue  # Si no se puede convertir, pasamos a la siguiente canción

        # Si el álbum aún no está en el diccionario, lo agregamos con valores iniciales
        if nombre_album not in albumes:
            albumes[nombre_album] = {
                "cantidad_canciones": 0,
                "duracion_total_ms": 0
            }

        # Incrementamos el contador de canciones y sumamos la duración total en milisegundos
        albumes[nombre_album]["cantidad_canciones"] += 1
        albumes[nombre_album]["duracion_total_ms"] += duracion_ms

    # Mostramos en pantalla el total de álbumes encontrados
    print(f"\nEl artista tiene {len(albumes)} álbum(es):\n")

    # Recorremos el diccionario de álbumes para mostrar los datos de cada uno
    for album, info in albumes.items():
        # Convertimos la duración total del álbum a HH:MM:SS
        duracion_formateada = ms_a_hhmmss(info["duracion_total_ms"])

        # Mostramos el nombre del álbum, la cantidad de canciones y la duración total
        print(f"Álbum: {album}")
        print(f"  Canciones: {info['cantidad_canciones']}")
        print(f"  Duración total: {duracion_formateada}\n")
