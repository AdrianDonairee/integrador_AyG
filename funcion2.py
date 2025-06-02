import csv
from datetime import timedelta

# Función que muestra el top 10 de canciones según coincidencias con artista o canción
def top_10_artista():
    # Se pide al usuario un término de búsqueda
    artista_input = input("Ingresá el nombre del artista o parte de una canción: ").strip()
    if not artista_input:
        print("No ingresaste ningún texto.")
        return

    canciones = []  # Lista para almacenar coincidencias

    try:
        with open("C:/Users/anchi/OneDrive/Escritorio/Facultad/3ro/automatas y gramaticas/tp4/TrabajoIntegrador/datos_spotify.csv", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)

            for fila in lector:
                # Convertimos las claves a minúsculas
                fila = {k.lower(): v for k, v in fila.items() if k is not None}

                # Obtenemos campos relevantes
                artista = str(fila.get("artist", "")).strip()
                cancion = str(fila.get("track", "")).strip()
                duracion_ms = str(fila.get("duration_ms", "0")).strip()

                # Buscamos coincidencia parcial en artista o título
                if artista_input.lower() in artista.lower() or artista_input.lower() in cancion.lower():
                    try:
                        # Convertimos duración a hh:mm:ss
                        duracion_segundos = int(float(duracion_ms)) // 1000
                        duracion_formateada = str(timedelta(seconds=duracion_segundos))
                        if len(duracion_formateada.split(":")) == 2:
                            duracion_formateada = "0:" + duracion_formateada

                        # Buscamos la mejor fuente de reproducciones
                        stream = fila.get("stream")
                        views = fila.get("views")
                        likes = fila.get("likes")
                        reproducciones = 0
                        if stream:
                            reproducciones = int(stream.replace(",", "").replace(".", "").strip())
                        elif views:
                            reproducciones = int(views.replace(",", "").replace(".", "").strip())
                        elif likes:
                            reproducciones = int(likes.replace(",", "").replace(".", "").strip())

                        # Guardamos el resultado
                        canciones.append((reproducciones, artista, cancion, duracion_formateada))
                    except:
                        continue
    except FileNotFoundError:
        print("No se encontró el archivo 'datos_spotify.csv'.")
        return

    if not canciones:
        print("No se encontraron coincidencias.")
        return

    # Ordenamos por reproducciones y mostramos top 10
    canciones.sort(reverse=True)
    top_10 = canciones[:10]

    print("\nTop 10 resultados:")
    for i, (reproducciones, artista, cancion, duracion) in enumerate(top_10, start=1):
        reproducciones_millones = f"{reproducciones / 1_000_000:.2f} M"
        print(f"{i}. Artista: {artista} | Canción: {cancion} | Duración: {duracion} | Reproducciones: {reproducciones_millones}")
