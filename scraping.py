from funciones_scraping import MAX_RESULTADOS, scrapear_libros
from funciones_busqueda import buscar_por_titulo, buscar_por_tematica, buscar_por_descripcion
from funciones_filtros import filtrar_por_anio, filtrar_por_formato
from funciones_mostrar import mostrar_resultados

# ------------------------- Menús -------------------------
def menu_principal():
    libros = []
    while True:
        print("\n=== MENÚ PRINCIPAL ===")
        print("1. Iniciar una búsqueda en Online Books")
        print("2. Salir")
        opcion = input("Elegí una opción: ")

        if opcion == "1":
            libros = iniciar_scraping()
            menu_busqueda(libros)
        elif opcion == "2":
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida, intentá de nuevo.")


def iniciar_scraping():
    autor = input("Autor (vacío para listados generales): ").strip()
    titulo = input("Palabra o frase del título (vacío para omitirla): ").strip()
    anio_min = leer_anio("Año mínimo (vacío para omitirlo): ")
    anio_max = leer_anio("Año máximo (vacío para omitirlo): ")
    formato = input("Formato (PDF, HTML, imágenes u otro; vacío para omitirlo): ").strip()

    print("\nCantidad máxima:")
    for indice, cantidad in enumerate(MAX_RESULTADOS, start=1):
        print(f"{indice}. {cantidad}")
    cantidad = elegir_cantidad()

    print("\nModo de selección:")
    print("1. Primeros resultados")
    print("2. Resultados aleatorios")
    aleatorio = input("Elegí una opción: ").strip() == "2"

    orden = elegir_orden()

    return scrapear_libros(
        cantidad,
        autor=autor,
        titulo=titulo,
        anio_min=anio_min,
        anio_max=anio_max,
        formato=formato,
        aleatorio=aleatorio,
        orden=orden,
    )


def leer_anio(mensaje):
    while True:
        valor = input(mensaje).strip()
        if not valor:
            return None
        try:
            return int(valor)
        except ValueError:
            print("Ingresá un año válido o dejá el campo vacío.")


def elegir_cantidad():
    while True:
        opcion = input("Elegí una opción: ").strip()
        try:
            cantidad = MAX_RESULTADOS[int(opcion) - 1]
            return cantidad
        except (ValueError, IndexError):
            print("Elegí una cantidad válida.")


def elegir_orden():
    print("\nOrden de resultados:")
    print("1. Orden original")
    print("2. Título")
    print("3. Autor")
    print("4. Año")
    opciones = {"1": "ninguno", "2": "titulo", "3": "autor", "4": "anio"}
    while True:
        opcion = input("Elegí una opción: ").strip()
        if opcion in opciones:
            return opciones[opcion]
        print("Elegí un orden válido.")


def menu_busqueda(libros):
    while True:
        print("\n=== MENÚ DE BÚSQUEDA Y FILTROS ===")
        print("1. Buscar por título")
        print("2. Buscar por autor")
        print("3. Buscar en la descripción")
        print("4. Filtrar por año")
        print("5. Filtrar por formato")
        print("6. Mostrar todos los libros")
        print("7. Volver al menú principal")
        opcion = input("Elegí una opción: ")

        if opcion == "1":
            buscar_por_titulo(libros)
        elif opcion == "2":
            buscar_por_tematica(libros)
        elif opcion == "3":
            buscar_por_descripcion(libros)
        elif opcion == "4":
            filtrar_por_anio(libros)
        elif opcion == "5":
            filtrar_por_formato(libros)
        elif opcion == "6":
            mostrar_resultados(libros)
        elif opcion == "7":
            break
        else:
            print("Opción inválida, intentá de nuevo.")

# ------------------------- Ejecución -------------------------
if __name__ == "__main__":
    menu_principal()
