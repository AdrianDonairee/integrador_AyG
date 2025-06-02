# Importamos módulos necesarios
import csv  # Para leer y escribir archivos CSV
import os   # Para comprobar existencia de archivos y su tamaño
import re   # Para trabajar con expresiones regulares

# Ruta al archivo CSV principal donde se almacenarán los registros
ARCHIVO = "C:/Users/anchi/OneDrive/Escritorio/Facultad/3ro/automatas y gramaticas/tp4/archivos comentados/datos_spotify.csv"

# Definimos la función para insertar registros
def insertar_registro():
    # Patrón para validar URLs (comienzan con http o https)
    patron_url = re.compile(r"^https?://\S+$")
    # Patrón para validar URI de Spotify (formato: spotify:track:XXX)
    patron_uri_spotify = re.compile(r"^spotify:track:[\w\d]+$")

    # Lista con los nombres de los campos del archivo CSV
    CAMPOS = ["artist", "track", "album", "uri", "duration_ms", "url_spotify", "url_youtube", "likes", "views"]

    # Mostrar menú de inserción
    print("\n--- Insertar nuevo registro ---")
    print("1. Ingresar manualmente")
    print("2. Cargar desde archivo CSV")

    # Se pide al usuario que elija una opción
    opcion = input("Elegí una opción (1 o 2): ").strip()

    # Si elige ingresar manualmente los datos
    if opcion == "1":
        # Se solicitan los datos uno por uno
        artista = input("Artista: ").strip()
        track = input("Título de la canción: ").strip()
        album = input("Álbum: ").strip()
        uri = input("URI de Spotify (spotify:track:XXX): ").strip()
        url_spotify = input("URL de Spotify: ").strip()
        url_youtube = input("URL de YouTube: ").strip()

        # Se intenta convertir los valores numéricos
        try:
            duracion_seg = int(input("Duración (en segundos): ").strip())
            likes = int(input("Cantidad de likes: ").strip())
            views = int(input("Cantidad de views: ").strip())
        except ValueError:
            print("Duración, likes y views deben ser números.")
            return

        # Validaciones usando expresiones regulares
        if not patron_uri_spotify.fullmatch(uri):
            print("URI de Spotify inválida.")
            return
        if not patron_url.fullmatch(url_spotify):
            print("URL de Spotify inválida.")
            return
        if not patron_url.fullmatch(url_youtube):
            print("URL de YouTube inválida.")
            return
        if likes > views:
            print("Error: los likes no pueden superar las views.")
            return

        # Se convierte duración de segundos a milisegundos
        duracion_ms = duracion_seg * 1000

        # Se construye un nuevo registro como diccionario
        nuevo = {
            "artist": artista,
            "track": track,
            "album": album,
            "uri": uri,
            "duration_ms": str(duracion_ms),
            "url_spotify": url_spotify,
            "url_youtube": url_youtube,
            "likes": str(likes),
            "views": str(views)
        }

        # Verificamos si se necesita escribir encabezado
        escribir_encabezado = not os.path.exists(ARCHIVO) or os.stat(ARCHIVO).st_size == 0

        try:
            # Abrimos el archivo en modo adjuntar
            with open(ARCHIVO, "a", newline='', encoding="utf-8") as archivo:
                escritor = csv.DictWriter(archivo, fieldnames=CAMPOS)
                if escribir_encabezado:
                    escritor.writeheader()  # Escribimos encabezado si es necesario
                escritor.writerow(nuevo)  # Escribimos el nuevo registro
                print("Registro insertado correctamente.")
        except Exception as e:
            print(f"Error al guardar el registro: {e}")

    # Si elige cargar desde un archivo CSV
    elif opcion == "2":
        ruta = input("Ruta del archivo CSV a importar: ").strip()
        # Validamos que el archivo exista
        if not os.path.exists(ruta):
            print("El archivo no existe.")
            return

        registros_validos = []  # Lista para almacenar registros válidos

        # Abrimos el archivo de origen
        with open(ruta, encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                try:
                    # Leemos los datos y limpiamos espacios
                    artista = fila.get("Artist", "").strip()
                    track = fila.get("Track", "").strip()
                    album = fila.get("Album", "").strip()
                    uri = fila.get("Uri", "").strip()
                    url_spotify = fila.get("Url_spotify", "").strip()
                    url_youtube = fila.get("Url_youtube", "").strip()
                    duracion_seg = int(fila.get("Duracion", "0").strip())
                    likes = int(fila.get("Likes", "0").strip())
                    views = int(fila.get("Views", "0").strip())
                except:
                    continue  # Si hay error en el registro, se salta

                # Validaciones de URI, URLs y coherencia entre likes y views
                if not patron_uri_spotify.fullmatch(uri):
                    continue
                if not patron_url.fullmatch(url_spotify) or not patron_url.fullmatch(url_youtube):
                    continue
                if likes > views:
                    continue

                # Convertimos duración y construimos diccionario con los datos
                duracion_ms = duracion_seg * 1000
                nuevo = {
                    "artist": artista,
                    "track": track,
                    "album": album,
                    "uri": uri,
                    "duration_ms": str(duracion_ms),
                    "url_spotify": url_spotify,
                    "url_youtube": url_youtube,
                    "likes": str(likes),
                    "views": str(views)
                }
                registros_validos.append(nuevo)  # Agregamos el registro a la lista

        # Si hay registros válidos, se escriben en el archivo principal
        if registros_validos:
            escribir_encabezado = not os.path.exists(ARCHIVO) or os.stat(ARCHIVO).st_size == 0

            try:
                with open(ARCHIVO, "a", newline='', encoding="utf-8") as archivo:
                    escritor = csv.DictWriter(archivo, fieldnames=CAMPOS)
                    if escribir_encabezado:
                        escritor.writeheader()
                    escritor.writerows(registros_validos)
                print(f"{len(registros_validos)} registros insertados correctamente.")
            except Exception as e:
                print(f"Error al guardar los registros: {e}")
        else:
            print("No se encontraron registros válidos.")
    else:
        # Si se eligió una opción inválida
        print("Opción no válida.")
