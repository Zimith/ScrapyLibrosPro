import requests
from bs4 import BeautifulSoup


def obtener_detalle_libro(url):
    try:
        respuesta = requests.get(url, timeout=10)
        respuesta.raise_for_status()
        soup = BeautifulSoup(respuesta.text, "html.parser")
        return "Libros en línea", soup.get_text(" ", strip=True)
    except requests.RequestException:
        return "Libros en línea", "Descripción no disponible."
