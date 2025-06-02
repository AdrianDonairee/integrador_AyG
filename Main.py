from funcion1 import buscar_por_titulo_o_artista
from funcion4 import mostrar_albumes
from funcion2 import top_10_artista
from funcion3 import insertar_registro



# Función que muestra el menú
def mostrar_menu():
    while True:
        print("\n--- MENÚ PRINCIPAL ---")
        print("1. Buscar por título o artista")
        print("2. Top 10 canciones de un artista")
        print("3. Insertar nuevo registro")
        print("4. Mostrar álbumes de un artista")
        print("5. Salir")

        opcion = input("Elegí una opción (1-5): ")
        if opcion == "1":
            buscar_por_titulo_o_artista()
        elif opcion == "2":
            top_10_artista()
        elif opcion == "3":
            insertar_registro()
        elif opcion == "4":
            mostrar_albumes()
        elif opcion == "5":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intentá de nuevo.")

mostrar_menu()