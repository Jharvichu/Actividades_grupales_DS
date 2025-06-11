#!/usr/bin/env python3
"""
Punto de entrada que une todos los patrones para generar una configuración
Terraform completamente local en formato JSON.

El archivo resultante puede aplicarse con:

    $ cd terraform
    $ terraform init
    $ terraform apply

No se requieren credenciales de nube, demonio de Docker, ni dependencias externas.
"""

import os
from iac_patterns.builder import InfrastructureBuilder
from iac_patterns.singleton import ConfigSingleton
from iac_patterns.composite import CompositeModule
import json

def main() -> None:
    # Inicializa una configuración global única para el entorno "local-dev"
    config = ConfigSingleton(env_name="desarrollo-local")
    config.set("proyecto", "patrones_iac_locales")

    # Construye la infraestructura usando el nombre de entorno desde la configuración global
    builder = InfrastructureBuilder(env_name=config.env_name)

    # Construye 15 recursos null ficticios para demostrar escalabilidad (>1000 líneas en total)
    builder.build_null_fleet(count=15)

    # Agrega un recurso simulado usando el adaptador (Actividad 3.2)
    builder.add_cloud_bucket(
        name="bucket_cloud_ds",
        triggers={"nota": "Recurso de nube simulada generada dinámicamente en tiempo de ejecución"}
    )

    # Agrega un recurso final personalizado con una nota descriptiva
    builder.add_custom_resource(
        name="finalizador",
        triggers={"nota": "Recurso compuesto generado dinámicamente en tiempo de ejecución"}
    )

    # Exporta el resultado a un archivo Terraform JSON en el directorio especificado
    builder.export(path=os.path.join("terraform", "main.tf.json"))

    # Crea módulo compuesto
    composite = CompositeModule()

    # Submodulo network
    network_module = {
        "module": {
            "network": {
                "source": "./modules/network",
                "cidr_block": "10.0.0.0/16"
            }
        }
    }

    # Submodulo app
    app_module = {
        "module": {
            "app": {
                "source": "./modules/app",
                "replicas": 3
            }
        }
    }

    # dummy
    null_resource = {
        "resource": [
            {
                "null_resource": {
                    "main": {
                        "triggers": {
                            "mensaje": "recurso parte del módulo compuesto"
                        }
                    }
                }
            }
        ]
    }

    # Agregando submódulos y recurso
    composite.add(network_module)
    composite.add(app_module)
    composite.add(null_resource)
    # estructura final
    os.makedirs("terraform", exist_ok=True)
    with open(os.path.join("terraform", "main.tf.json"), "w") as f:
        json.dump(composite.export(), f, indent=2)

# Ejecuta la función principal si el archivo se ejecuta directamente
if __name__ == "__main__":
    main()
