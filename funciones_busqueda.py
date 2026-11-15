from funciones_mostrar import mostrar_resultados
from funciones_scraping import normalizar_texto


def buscar_por_titulo(libros):
    palabra = normalizar_texto(input("Ingresá una palabra o parte del título: ").strip())
    resultados = [
        libro for libro in libros if palabra in normalizar_texto(libro["titulo"])
    ]
    mostrar_resultados(resultados)


def buscar_por_tematica(libros):
    palabra = normalizar_texto(input("Ingresá el autor: ").strip())
    resultados = [
        libro
        for libro in libros
        if palabra in normalizar_texto(libro["autor"])
    ]
    mostrar_resultados(resultados)


def buscar_por_descripcion(libros):
    palabra = normalizar_texto(input("Ingresá una palabra clave: ").strip())
    resultados = [
        libro
        for libro in libros
        if palabra in normalizar_texto(libro["descripcion"])
    ]
    mostrar_resultados(resultados)
