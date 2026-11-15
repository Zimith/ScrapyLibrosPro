import re


RESULTADOS_POR_PAGINA = 20


def normalizar_descripcion(descripcion):
    """Mejora expresiones bibliográficas conocidas sin alterar los datos."""
    reemplazos = (
        (r"\billust\.\s+by\b", "ilustrado por"),
        (r"\bmultiple formats at\b", "múltiples formatos disponibles en"),
        (r"\bpage images at\b", "imágenes de páginas disponibles en"),
    )
    resultado = descripcion
    for patron, reemplazo in reemplazos:
        resultado = re.sub(patron, reemplazo, resultado, flags=re.IGNORECASE)
    return resultado


def obtener_pagina(resultados, pagina, por_pagina=RESULTADOS_POR_PAGINA):
    inicio = pagina * por_pagina
    return resultados[inicio : inicio + por_pagina]


def imprimir_libro(indice, libro):
    print(f"{indice}. {libro['titulo']}")
    print(f"   Autor: {libro['autor']}")
    print(f"   Año: {libro['anio'] or 'No informado'}")
    print(f"   Formato: {libro['formato']}")
    print(f"   Descripción: {normalizar_descripcion(libro['descripcion'])}")
    print(f"   Enlace: {libro['enlace'] or 'No informado'}\n")


def mostrar_pagina(resultados, pagina, por_pagina=RESULTADOS_POR_PAGINA):
    inicio = pagina * por_pagina
    pagina_resultados = obtener_pagina(resultados, pagina, por_pagina)
    fin = inicio + len(pagina_resultados)
    total_paginas = (len(resultados) + por_pagina - 1) // por_pagina

    print(
        f"\nPágina {pagina + 1} de {total_paginas} "
        f"(resultados {inicio + 1}-{fin} de {len(resultados)}):\n"
    )
    for indice, libro in enumerate(pagina_resultados, start=inicio + 1):
        imprimir_libro(indice, libro)


def mostrar_resultados(resultados):
    if not resultados:
        print("\nNo se encontraron resultados.\n")
        return

    print(f"\nSe encontraron {len(resultados)} resultados:\n")
    total_paginas = (len(resultados) + RESULTADOS_POR_PAGINA - 1) // RESULTADOS_POR_PAGINA
    pagina = 0

    while True:
        mostrar_pagina(resultados, pagina)
        if total_paginas == 1:
            input("\nPresioná Enter para volver al menú anterior.")
            return

        print("\nOpciones: [s]iguiente, [a]nterior, [t]odos, [v]olver")
        opcion = input("Elegí una opción: ").strip().lower()
        if opcion == "s":
            if pagina < total_paginas - 1:
                pagina += 1
            else:
                print("Ya estás en la última página.")
        elif opcion == "a":
            if pagina > 0:
                pagina -= 1
            else:
                print("Ya estás en la primera página.")
        elif opcion == "t":
            for indice, libro in enumerate(resultados, start=1):
                imprimir_libro(indice, libro)
            input("Presioná Enter para volver a la navegación.")
        elif opcion == "v":
            return
        else:
            print("Opción inválida.")
