# Actividad 23: Pruebas en IaC

## Ejercicio 1: Estrategia de "pruebas unitarias" y "pruebas de contrato" combinadas

### 1. Diseño de módulos declarativos

Si se quiere realizar pruebas de manera aislada para tres módulos terraform, entonces cada uno de estos debería de mostrar una interfaz clara, usando variables de entrada y outputs correctamente definidos:

1. **`network`**:
	- Variables:
		- `cidr_vpc`: Para definir el rango de IP´s privadas para la VPC. Es una variable importante ya que nos permite delimitar el espacio de la red, además de evitar el solapamiento con otras redes.
		- `cidr_subnets`: Es una lista de CIDR´s para la creación de redes dentro de la VPC. Nos permite dividir la red y aislar recursos dependiendo de los propósitos.
		- `tags`: Serían etiquetas que se aplicarían a todos los recursos del módulo para hacer más fácil la identificación.
	- Outputs:
		- `id_vpc`: Es el ID, único, de la VPC que se crea. Es importante ya que esta ID será necesaria para que otros módulos puedan referenciar instancias o recursos de la red.
		- `ids_subnet`: Es una lista de ID´s de las subredes generadas. Nos permite la conexión entre los módulos de `compute` o `storage` se conecten a segmentos de la red.

2. **`compute`**:
	- Variables:
		- `id_image`: Es un identificador de la imagen del SO que se usa, o de un contenedor. Acá se define la base del software, para los recursos de cómputo.
		- `instance_type`: Para especificar las características de la máquina virtual (RAM, CPU, etc.). También, permite modificar el recurso para adaptarlo a las necesidades.
		- `id_subnet`: Es la ID de la subred donde se va a desplegar la instancia. Esto nos asegura el aislamiento de red, además de una buena integración con el módulo `network`
	- Outputs:
		- `id_instance`: Es la ID de la instancia que se crea, esto será necesario para las actividades de monitoreo y automatización.
		- `ip_private`: Es la dirección IP privada que se le asigna a la instancia, es importante para la comunicación interna, además que sirve para las prebas de conectividad.

3. **`storage`**:
	- Variables:
		- `bucket_name`: Es un nombre único que se le asigna al recurso de almacenamiento. Se puede ver como una "ID", que servirá para referenciar al `storage` desde otros módulos.
		- `versioning`: Es un booleano e indicará si se habilita o no el versionado de objetos, para garantizar integridad como también la recuperación en caso de errores.
	- Outputs:
		- `id_bucket`: Es un ID para el bucket, y es necesario para las operaciones cruzadas entre módulos.
		- `storage_data`: Contiene gran información como: las políticas de acceso, endpoints, etc., útil para la realización de pruebas automáticas.

***¿Qué convenios de naming y estructura de outputs pactarías para garantizar, a nivel de contrato, que diferentes equipos puedan reutilizar tus módulos sin integrarlos aún?***

Se pactarían convenciones, como la prefijación de outputs con el nombre del módulo donde esté (por ejemplo: `network_id_vpc`), además de la documentación de la estructura de cada output.

Ahora, los outputs complejos se mostrarían en formato JSON, con los campos bien documentados y versionados, para que los equipos encargados del consumo puedan validarlos sin necesitar de la implementación interna.

### 2. Caso límite sin recursos externos

#### Escenarios de inputs inválidos

Usando los módulos del inciso anterios:

- En el módulo `network`, un caso sería un CIDR que esté fuera de rango (*300.0.0.0/16*, por ejemplo), debería ser detectado como incorrecto/inválido.
- En el módulo `compute`, un caso sería pasar valores negativos a una instancia de conteo, esto debería invalidar el despliegue ya que no tendría sentido.
- En el módulo `storage`, si la variable `bucket_name` cuenta con caracteres no permitidos (espacios o mayúsculas), debería ser rechazado.

#### Herramientas y comandos

- Para validar sintaxis o estructuras básicas (como errores de formato, de escritura, etc.) es recomendable usar `terraform validate`.
- Para validar reglas semánticas (dependencias entre variables, restricciones de negocio, etc.) se podría combinar `terraform plan` (detectará recursos que no serán creados) con `terraform output -json` (para el análisis de los outputs generados).

### 3. Métrica de cobertura de contrato

Se plantaría una métrica que esté basada en la cantidad de outputs documentados que son verificados directamente por los tests. Dando un ejemplo, si un módulo tiene seis outputs documentados, y los tests automatizados validan solamente cinco de ellos, entonces la cobertura sería *5/6 <> 83%*

***¿Cómo balancearías la exhaustividad (todos los campos) con el costo de mantenimiento (cambios frecuentes en outputs)***

- Se priorizaría los outputs críticos de integración y también los outputs que son usados por otros equipos o módulos.
- Se documentaría con claridad los outputs que están relacionados a testing obligatorio y también los outputs que puedan validarse solo en la integración.
- Se automatizaría el reporte de cobertura con scripts que comparen la documentación de outputs con los outputs validados en los tests.


## Ejercicio 2: "Pruebas de integración" entre módulos

### 4. Secuenciación de dependencias

### 5. Entornos simulados con contenedores

### 6. Pruebas de interacción gradual

## Ejercicio 3: "Pruebas de humo" y "Pruebas de regresión"

### 7. Pruebas de humo locales ultrarrápidos

### 8. Planes "golden" para regresión

### 9. Actualización consciente de regresión

## Ejercicio 4: "Pruebas extremo-extremo (E2E)" y su rol en arquitecturas modernas

### 10. Escenarios E2E sin IaC real

**Test**

Se diseñaría un escenario E2E que consista en que, luego de aplicar los módulos terraform localmente, se despliegue el servicio flask dentro de un contenedor Docker. Este servicio simularía una aplicación real y la prueba consistiría en verificar la conectividad y configuración de la red, que fue generada por terraform.

**Métricas por examinar e integración**

- Código de estado HTTP (que espere código 200 en endpoints válidos y 404 para accesos restringidos).
- Latencia de respuesta (usando herramientas como `curl`).
- Formato y contenido de los JSON, validando que se cumpla con el contrato esperado.

Las métricas mencionadas pueden integrarse como scripts, luego de aplicar `terraform apply`. Estos scripts serían ejecutados localmente y mostrarían los resultados en la consola, sin la necesidad de pipelines CI externos.

### 11. E2E en microservicios y Kubernetes local

**Clúster local de Kubernetes**

Para validar despliegues complejos, se levantaría un cluster Kubernetes local. Y terraform sería el encargado de generar los YML o plantillas Helm.

### 12. Simulación de fallos en E2E

## Ejercicio 5: Pirámide de pruebas y selección de tests

### 13. Mapeo de pruebas al pipeline local

### 14. Estrategia de "test slices"

### 15. Coste vs. riesgo de tests

## Ejercicio 6: Estrategias de mantenimiento y evolución de la suite

### 16. Deuda técnica en pruebas IaC

### 17. Documentación viva de tests

### 18. Automatización local de la suite

## Ejercicio 7: Ampliación de módulos y pruebas unitarias "en caliente"

## Ejercicio 8: Contratos dinámicos y testing de outputs

## Ejercicio 9: Integración encadenada con entornos simulados

## Ejercicio 10: Pruebas de humo híbridos con Terraform

## Ejercicio 11: Pruebas de integración con "plan dorado" inteligentes

## Ejercicio 12: Flujo E2E local con microservicios simulados
