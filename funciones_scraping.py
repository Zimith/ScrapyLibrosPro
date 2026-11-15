import random
import re
import time
import unicodedata
from urllib.parse import urljoin, urlsplit, urlunsplit

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://onlinebooks.library.upenn.edu/"
BUSQUEDA_URL = urljoin(BASE_URL, "webbin/book/search")
NUEVOS_LIBROS_URL = urljoin(BASE_URL, "new.html")
MAX_RESULTADOS = (25, 50, 100, 200)
HEADERS = {"User-Agent": "Scraping-Libros/1.0 (proyecto educativo)"}


def scrapear_libros(
    cantidad,
    autor="",
    titulo="",
    anio_min=None,
    anio_max=None,
    formato="",
    aleatorio=False,
    orden="ninguno",
):
    """Obtiene libros desde el buscador o los listados HTML de Online Books."""
    if cantidad not in MAX_RESULTADOS:
        raise ValueError(f"La cantidad debe ser una de: {MAX_RESULTADOS}.")

    print(f"\nIniciando scraping de hasta {cantidad} libros...\n")
    inicio = time.time()

    try:
        if autor.strip() or titulo.strip():
            parametros = {
                "showtitles": "1",
                "amode": "words",
                "tmode": "words",
            }
            if autor.strip():
                parametros["author"] = autor.strip()
            if titulo.strip():
                parametros["title"] = titulo.strip()
            respuesta = requests.get(
                BUSQUEDA_URL, params=parametros, headers=HEADERS, timeout=20
            )
        else:
            respuesta = requests.get(NUEVOS_LIBROS_URL, headers=HEADERS, timeout=20)
        respuesta.raise_for_status()
    except requests.RequestException as error:
        print(f"No se pudo acceder a Online Books: {error}")
        return []

    soup = BeautifulSoup(respuesta.text, "html.parser")
    libros = []
    for elemento in soup.select("li"):
        libro = extraer_libro(elemento)
        if libro:
            libros.append(libro)

    libros = eliminar_duplicados(libros)
    libros = [
        libro
        for libro in libros
        if cumple_filtros(libro, anio_min, anio_max, formato)
    ]
    ordenar_libros(libros, orden)
    if aleatorio:
        random.shuffle(libros)
    libros = libros[:cantidad]

    print(
        f"\nScraping completado en {round(time.time() - inicio, 2)} segundos. "
        f"Total libros: {len(libros)}\n"
    )
    return libros


def extraer_libro(elemento):
    titulo = elemento.find("cite")
    if not titulo:
        titulo = elemento.find("a", href=re.compile(r"/(?:lookupid|work|gutbook)/"))
    if not titulo:
        return None

    titulo = titulo.get_text(" ", strip=True)
    enlace = elemento.find("a", href=lambda href: href and "lookupid" in href)
    texto = elemento.get_text(" ", strip=True)
    enlace_url = normalizar_url(enlace["href"]) if enlace else ""
    autor = extraer_autor(texto, titulo)
    anio = extraer_anio(texto, titulo)
    formato = extraer_formato(texto)

    return {
        "titulo": titulo,
        "autor": autor,
        "anio": anio,
        "categoria": "Libros en línea",
        "formato": formato,
        "descripcion": texto,
        "enlace": enlace_url,
    }


def extraer_autor(texto, titulo):
    antes_del_titulo = texto.split(titulo, 1)[0].strip()
    if ":" in antes_del_titulo:
        autor = antes_del_titulo.rstrip(":").strip()
        autor = re.sub(r",\s*(?:ed|trans|contrib|illust)\.\s*$", "", autor)
        if autor:
            return autor

    despues_del_titulo = texto.split(titulo, 1)[-1]
    coincidencia = re.search(
        r"(?:^|,\s*|\s)\b(?:ed\.\s+by|by)\s+(.+?)(?=,\s*(?:ed|trans|contrib|illust)\.\s+by|\s*,?\s+also\s+by|\s+(?:multiple formats|page images|PDF|HTML|Gutenberg|at )|\s*\(|$)",
        despues_del_titulo,
        re.IGNORECASE,
    )
    return coincidencia.group(1).strip(" ,") if coincidencia else "Autor no disponible"


def extraer_anio(texto, titulo=""):
    segmento = texto.split(titulo, 1)[-1] if titulo else texto
    parentesis = re.search(r"\(([^)]*)\)", segmento)
    fuente = parentesis.group(1) if parentesis else segmento
    coincidencias = re.findall(r"\b(?:1[5-9]\d{2}|20\d{2})\b", fuente)
    return int(coincidencias[0]) if coincidencias else None


def extraer_formato(texto):
    formatos = []
    for etiqueta, patron in (
        ("PDF", r"\bPDF\b"),
        ("HTML", r"\bHTML\b"),
        ("Imágenes", r"page images"),
        ("Múltiples formatos", r"multiple formats"),
    ):
        if re.search(patron, texto, re.IGNORECASE):
            formatos.append(etiqueta)
    return ", ".join(formatos) if formatos else "No disponible"


def cumple_filtros(libro, anio_min=None, anio_max=None, formato=""):
    if anio_min is not None and (
        libro["anio"] is None or libro["anio"] < anio_min
    ):
        return False
    if anio_max is not None and (
        libro["anio"] is None or libro["anio"] > anio_max
    ):
        return False
    if not formato.strip():
        return True
    buscado = normalizar_texto(formato)
    texto_formato = normalizar_texto(libro["formato"])
    equivalencias = {
        "pdf": "pdf",
        "html": "html",
        "imagen": "imagenes",
        "imagenes": "imagenes",
        "page images": "imagenes",
        "multiple": "multiples formatos",
        "multiples formatos": "multiples formatos",
    }
    return equivalencias.get(buscado, buscado) in texto_formato


def normalizar_texto(texto):
    return "".join(
        caracter
        for caracter in unicodedata.normalize("NFKD", texto.lower())
        if not unicodedata.combining(caracter)
    )


def normalizar_url(url):
    if not url:
        return ""
    completa = urljoin(BASE_URL, url)
    partes = urlsplit(completa)
    ruta = partes.path.replace("/book//lookupid", "/book/lookupid")
    return urlunsplit((partes.scheme.lower(), partes.netloc.lower(), ruta, partes.query, ""))


def eliminar_duplicados(libros):
    vistos = set()
    unicos = []
    for libro in libros:
        identificador = libro["enlace"] or (
            normalizar_texto(libro["titulo"]),
            normalizar_texto(libro["autor"]),
            libro["anio"],
        )
        if identificador not in vistos:
            vistos.add(identificador)
            unicos.append(libro)
    return unicos


def ordenar_libros(libros, orden):
    claves = {
        "titulo": lambda libro: (not libro["titulo"], normalizar_texto(libro["titulo"])),
        "autor": lambda libro: (not libro["autor"], normalizar_texto(libro["autor"])),
        "anio": lambda libro: (libro["anio"] is None, libro["anio"] or 0),
    }
    if orden in claves:
        libros.sort(key=claves[orden])
