#!/usr/bin/env python3

import json
import os
import requests
import sys

def buscar_configuraciones(directorio='generated_environment/services'):
    archivos = []
    for raiz, dirs, files in os.walk(directorio):
        for archivo in files:
            if archivo == "config.json":
                archivos.append(os.path.join(raiz, archivo))
    return archivos

def main():
    codigo_salida = 0
    archivos_config = buscar_configuraciones()
    if not archivos_config:
        print("Error: No hay archivos de configuracion")
        sys.exit(1)
    for ruta_config in archivos_config:
        with open(ruta_config, "r") as f:
            configuracion = json.load(f)
        if "api_endpoints" not in configuracion:
            print(f"No hay endpoints")
            continue
        for endpoint in configuracion["api_endpoints"]:
            url = endpoint.get("url")
            nombre = endpoint.get("name", "desconocido")
            try:
                respuesta = requests.get(url, timeout=2)
                if respuesta.status_code == 200:
                    try:
                        datos = respuesta.json()
                        print(f"Endpoint '{nombre}' responde correctamente con json")
                    except Exception:
                        print(f"Error: El endpoint '{nombre}' no hay json valido")
                        codigo_salida = 5
                else:
                    print(f"El endpoint '{nombre}' devolvió código {respuesta.status_code}")
                    codigo_salida = 3
            except Exception as e:
                print(f"No se pudo conectar a {url}: {e}")
                codigo_salida = 2

    sys.exit(codigo_salida)


if __name__ == "__main__":
    main()