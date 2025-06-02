# Importamos el módulo 'csv' para trabajar con archivos CSV
import csv

# Importamos 'timedelta' de la biblioteca 'datetime' para formatear la duración en formato legible
from datetime import timedelta

# Definimos una función para buscar canciones o artistas por nombre
def buscar_por_titulo_o_artista():
    # Solicitamos al usuario que ingrese el título o artista a buscar, eliminamos espacios y convertimos a minúsculas
    termino = input("Ingresá el título o artista a buscar: ").strip().lower()
    
    # Verificamos si el usuario no ingresó ningún texto
    if not termino:
        print("No ingresaste ningún texto.")
        return  # Salimos de la función si no hay término de búsqueda

    # Creamos una lista vacía para almacenar los resultados encontrados
    resultados = []

    try:
        # Abrimos el archivo CSV con codificación UTF-8
        with open("C:/Users/anchi/OneDrive/Escritorio/Facultad/3ro/automatas y gramaticas/tp4/archivos comentados/datos_spotify.csv", encoding="utf-8") as archivo:
            # Usamos DictReader para leer el archivo como diccionarios (clave-valor)
            lector = csv.DictReader(archivo)

            # Iteramos sobre cada fila del archivo
            for fila in lector:
                # Convertimos todas las claves del diccionario a minúsculas
                fila = {k.lower(): v for k, v in fila.items() if k is not None}

                # Obtenemos y limpiamos los valores de artista, canción y duración
                artista = str(fila.get("artist", "")).strip()
                cancion = str(fila.get("track", "")).strip()
                duracion_ms = str(fila.get("duration_ms", "0")).strip()

                # Verificamos si el término de búsqueda está en el nombre del artista o de la canción
                if termino in artista.lower() or termino in cancion.lower():
                    try:
                        # Convertimos la duración de milisegundos a segundos y luego la formateamos
                        duracion_segundos = int(float(duracion_ms)) // 1000
                        duracion_formateada = str(timedelta(seconds=duracion_segundos))

                        # Si la duración tiene solo minutos y segundos (sin horas), le agregamos "0:" al inicio
                        if len(duracion_formateada.split(":")) == 2:
                            duracion_formateada = "0:" + duracion_formateada

                        # Obtenemos posibles campos de cantidad de reproducciones
                        stream = fila.get("stream")
                        views = fila.get("views")
                        likes = fila.get("likes")
                        reproducciones = 0  # Valor por defecto

                        # Si el campo 'stream' existe, lo usamos como cantidad de reproducciones
                        if stream:
                            reproducciones = int(stream.replace(",", "").replace(".", "").strip())
                        # Si no, probamos con el campo 'views'
                        elif views:
                            reproducciones = int(views.replace(",", "").replace(".", "").strip())
                        # Y si no, con el campo 'likes'
                        elif likes:
                            reproducciones = int(likes.replace(",", "").replace(".", "").strip())

                        # Agregamos una tupla con los datos encontrados a la lista de resultados
                        resultados.append((reproducciones, artista, cancion, duracion_formateada))
                    except Exception:
                        # Si ocurre algún error durante la conversión o lectura de datos, lo ignoramos y seguimos
                        continue
    except FileNotFoundError:
        # Si no se encuentra el archivo CSV, mostramos un mensaje de error
        print("No se encontró el archivo 'datos_spotify.csv'.")
        return

    # Si no se encontraron coincidencias, informamos al usuario
    if not resultados:
        print("No se encontraron resultados.")
        return

    # Ordenamos los resultados por cantidad de reproducciones en orden descendente
    resultados.sort(reverse=True)

    # Mostramos los resultados al usuario
    print("\nResultados:")
    for reproducciones, artista, cancion, duracion in resultados:
        print(f"Artista: {artista} | Canción: {cancion} | Duración: {duracion}")
