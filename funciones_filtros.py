from funciones_mostrar import mostrar_resultados
from funciones_scraping import normalizar_texto


def filtrar_por_anio(libros):
    try:
        anio_min_texto = input("Ingresá el año mínimo (vacío para omitirlo): ").strip()
        anio_max_texto = input("Ingresá el año máximo (vacío para omitirlo): ").strip()
        anio_min = int(anio_min_texto) if anio_min_texto else None
        anio_max = int(anio_max_texto) if anio_max_texto else None
    except ValueError:
        print("Ingresá años válidos.")
        return

    resultados = [
        libro
        for libro in libros
        if (anio_min is None or (libro["anio"] is not None and libro["anio"] >= anio_min))
        and (anio_max is None or (libro["anio"] is not None and libro["anio"] <= anio_max))
    ]
    mostrar_resultados(resultados)


def filtrar_por_formato(libros):
    categoria = normalizar_texto(
        input("Ingresá el formato (PDF, HTML, imágenes): ").strip()
    )
    resultados = [
        libro
        for libro in libros
        if categoria in normalizar_texto(libro["formato"])
    ]
    mostrar_resultados(resultados)
