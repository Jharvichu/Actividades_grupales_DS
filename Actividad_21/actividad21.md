# ACTIVIDAD 21

## Fase 1: Exploración y análisis

### 1.1. Singleton

### 1.2. Factory
La fábrica(Factory) encapsula la creación del Null Resource de 4 maneras.

La primera manera de encapsulación es mediante la Abstracción de la estructura interna, la fábrica proporciona un método llamado create(), simplemente el usuario tiene que proporcionar su nombre.

La segunda manera de encapsulación se da cuando la fábrica genera datos para los triggers. En  factory_uuid se crea un UUID usando uuid. uuid4(), esto hace que cada null_resource recientemente dado por la fábrica, pose a un identificador único en sus triggers. El timestamp() registra el tiempo UTC actual. La tercera manera se da cuando la fábrica se preocupa para que todos los null_resource  usen una misma estructura y convención. La última forma de encapsular se da cuando la estructura de null_resource cambia debido a que se le agregaron nuevas propiedades o se le modifico la manera en que se definieron triggers.

Los triggers tienen como propósito no actuar directamente sobre la infraestructura, sino más bien controlar el ciclo de vida de las acciones que tienen que ver con null_resource, pueden hacer que se pueda volver a ejecutar ciertos scripts.

### 1.3. Prototype

### 1.4. Composite

### 1.5. Builder
Builder orquesta al composite creando una instancia de CompositeModule, este es importante para agrupar muchos elementos de  infraestructura , acá son recursos, dentro de una estructura jerárquica. Esto hace que Builder pueda adicionar muchos recursos y los pueda exportar.

Se orquesta Factory cuando Builder delega la creación de la estructura base de un null resource a NullResourceFactory. La fábrica NullResourceFactory se encarga de crear la estructura del null_resource con ayuda de sus triggers(UUID y timestamp). Todo esto encapsula lo difícil de formar un null_resource y da una base limpia. Este Builder no  necesita saber mucho acerca de la creación del null_resource, solo la fábrica devolverá un objeto null_resource válido.

 Orquestar Prototipo, es un proceso diferente, pues primero que Builder posee la base(null_resource), la usa para inventar ResourcePrototype. El Patrón Prototype es muy importante para mejorar la eficiencia del trabajo. Para que count no cree nuevos null_resurce desde el comienzo con la fábrica, lo cual es muy costoso, el Builder crea un prototipo del recurso.

Nuevamente se hace orquestacion del composite(), para esto primero Builder  llama a el método export() de su self.module().Para esto de aca, se espera  con ansias que CompositeModule.export() otorgue  un diccionario que represente la estructura JSON final de la infraestructura.

Ya por fin se genera el JSON . Finalmente, el Builder toma esta estructura de datos devuelta por el CompositeModule y la escribe en un archivo JSON utilizando json.dump(), con una indentación de 2 para facilitar la lectura.

## Fase 2: Ejercicios prácticos

### Ejercicio 2.1: Extensión del Singleton

Primero, añadimos un nuevo método a `singleton.py` llamado `reset()`. Su función será limpiar `settings` pero manteniendo `created_at`.

```python
def reset(self) -> None:
    self.settings.clear()
```

Luego, para validar esta función se crea un nuevo directorio `tests/` donde se creará el archivo `test_singleton.py`. Ahi es donde se realizará el test para probar que la nueva función añadida funciona correctamente.

```python
from iac_patterns.singleton import ConfigSingleton 
import datetime

def test_reset():
    c1 = ConfigSingleton("dev")
    created = c1.created_at
    c1.settings["x"] = 1
    c1.reset()
    assert c1.settings == {}
    assert c1.created_at == created

if __name__ == "__main__":
    test_reset()
```

Al ejecutarlo, notamos que el test pasa, lo cual indica que el método funciona correctamente.

<div align = "center">
    <img src="img/ejer2_1.png" width="500">
</div>

### Ejercicio 2.2: Variación de la Factory



### Ejercicio 2.3: Mutaciones avanzadas con Protype


Agregue este método dentro del archivo Prototype.py.

Primero se tiene un diccionario dentro del método(da una configuracion de recursos de Terraform).  Se hacen cambios a los triggers de un recurso null_resource

Al final se grega un recurso local file, que tiene como funcion agregar un archivo de texto


```python
def add_welcome_file(block: dict):

        block["resource"]["null_resource"]["app_0"]["triggers"]["welcome"] = "¡Hola!"

        block["resource"]["local_file"] = {

        "welcome_txt": {

            "content": "Bienvenido",

            "filename": "${path.module}/bienvenida.txt"

        }

    }
```


Dentro de main.tf.json  agregue el bloque local_file, para que me compile un archivo de bienvenida.txt, con su mensaje “¡Hola, bienvenida!”


```
{

            "local_file": {

                "bienvenida": {

                    "content": "¡Hola, bienvenida!",

                    "filename": "${path.module}/bienvenida.txt"

                }

            }

        }
```


Me fui a mi ruta de Terraform y active el entorno virtual .venv.

Primero hice “terraform init" , luego  “terraform plan”,  al final ejecuto Terraform mediante "Terraform Apply".





![cc](https://github.com/Jharvichu/Actividades_grupales_DS/blob/main/Actividad_21/img/2.3.1.png)



Se ejecuto perfectamente bien “Terraform Apply”



![io](https://github.com/Jharvichu/Actividades_grupales_DS/blob/main/Actividad_21/img/2.3.2.png)



Se generó un archivo de bienvenida.txt, tal como se tenía planeado desde que se agrego el bloque “local_file” .



![pp](https://github.com/Jharvichu/Actividades_grupales_DS/blob/main/Actividad_21/img/2.3.3.png)





### Ejercicio 2.4: Submódulos con Composite



### Ejercicio 2.5: Builder personalizado



## Fase 3: Desafíos teórico-prácticos

### 3.1. Comparativa Factory vs Prototype



### 3.2 Patrones avanzados: Adapter (código de referencia)
Primero cree el archivo adapter.py dentro de iac_patterns 

```python

adapter.py

class MockBucketAdapter: def init(self, null_block: dict): self.null = null_block 

def to_bucket(self) -> dict:
    # Mapear triggers a parámetros de bucket simulado
    name = list(self.null["resource"]["null_resource"].keys())[0] 
    return {
        "resource": {
            "mock_cloud_bucket": {
                name: {"name": name, **self.null["resource"]["null_resource"][name]["triggers"]} 
            }
        }
    }

```

 

 

La clase MockBucketAdapter toma un bloque de configuración de Terraform que usa null_resource y lo convierte en un recurso simulado llamado mock_cloud_bucket.

En concreto:

Extrae el nombre del recurso null_resource.

Copia los valores definidos en triggers.

Crea un nuevo diccionario con formato de bucket simulado, incluyendo el nombre y esos valores. 

  

Hize cambios en builder.py :

 

```python

from iac_patterns.adapter import MockBucketAdapter

```

 

 

Cree la clase Builder dentreo de Builder.py :

 

```python

class Builder:

    def __init__(self):
        self.infra = {}

    def add_null(self, name, triggers=None):
        null_factory = NullFactory(name, triggers)
        resource = null_factory.create()
        self.infra.update(resource)

    def add_mock_bucket(self, name, triggers=None):
        null_factory = NullFactory(name, triggers)
        null_resource = null_factory.create()
        adapter = MockBucketAdapter(null_resource)
        mock_bucket_resource = adapter.to_bucket()
        self.infra.update(mock_bucket_resource)

    def generate(self):
        return self.infra

```



La clase Builder sirve para crear y almacenar diferentes recursos de infraestructura en un diccionario llamado infra.

add_null(name, triggers=None):
 Crea un recurso "null" usando una fábrica (NullFactory), y lo añade al diccionario infra.

add_mock_bucket(name, triggers=None):
 Primero crea un recurso "null" con NullFactory. Luego, usa un adaptador (MockBucketAdapter) para convertir ese recurso "null" en un recurso tipo "mock bucket". Finalmente, añade este recurso transformado al diccionario infra.

generate():
 Devuelve la infraestructura completa que se ha ido construyendo (el diccionario infra).

  

 

Luego ejecute:



![oo](https://github.com/Jharvichu/Actividades_grupales_DS/blob/main/Actividad_21/img/3.2.1.png)



todo exitoso el resultado.



![om](https://github.com/Jharvichu/Actividades_grupales_DS/blob/main/Actividad_21/img/3.2.2.png)


Primero cree el archivo adapter.py dentro de iac_patterns y le implemente este método: 

```python 

adapter.py 

class MockBucketAdapter: def init(self, null_block: dict): self.null = null_block 

def to_bucket(self) -> dict: 
    # Mapear triggers a parámetros de bucket simulado 
    name = list(self.null["resource"]["null_resource"].keys())[0] 
    return { 
        "resource": { 
            "mock_cloud_bucket": { 
                name: {"name": name, **self.null["resource"]["null_resource"][name]["triggers"]} 
            } 
        } 
    } 

``` 

 

 

La clase MockBucketAdapter toma un bloque de configuración de Terraform que usa null_resource y lo convierte en un recurso simulado llamado mock_cloud_bucket. 

En resumen:
Extrae el nombre del recurso null_resource. Copia los valores definidos en triggers. Crea un nuevo diccionario con formato de bucket simulado, incluyendo el nombre y esos valores. 

  
Hize cambios en builder.py : 

 

```python 

from iac_patterns.adapter import MockBucketAdapter 

``` 




Cree la clase Builder dentreo de Builder.py : 

 

```python 

class Builder: 

    def __init__(self): 

        self.infra = {} 

 

    def add_null(self, name, triggers=None): 

        null_factory = NullFactory(name, triggers) 

        resource = null_factory.create() 

        self.infra.update(resource) 


    def add_mock_bucket(self, name, triggers=None): 

        
        null_factory = NullFactory(name, triggers) 

        null_resource = null_factory.create() 

        adapter = MockBucketAdapter(null_resource) 

        mock_bucket_resource = adapter.to_bucket()      

        self.infra.update(mock_bucket_resource) 

 

    def generate(self): 

        return self.infra  
 
``` 

 


La clase Builder sirve para crear y almacenar diferentes recursos de infraestructura en un diccionario llamado infra. 

add_null(name, triggers=None): 
 Crea un recurso "null" usando una fábrica (NullFactory), y lo añade al diccionario infra. 

add_mock_bucket(name, triggers=None): 
 Primero crea un recurso "null" con NullFactory. Luego, usa un adaptador (MockBucketAdapter) para convertir ese recurso "null" en un recurso tipo "mock bucket". Finalmente, añade este recurso transformado al diccionario infra. 

generate(): 
 Devuelve la infraestructura completa que se ha ido construyendo (el diccionario infra). 

Luego ejecute Terraform:



![io](https://github.com/Jharvichu/Actividades_grupales_DS/blob/main/Actividad_21/img/3.2.1.png)

 


y salio todo bien:





![òp](https://github.com/Jharvichu/Actividades_grupales_DS/blob/main/Actividad_21/img/3.2.2.png)






### 3.3 Tests automatizados con pytest



### 3.4 Escalabilidad de JSON


### 3.5 Integración con Terraform Cloud(opcional)


![yu](https://github.com/Jharvichu/Actividades_grupales_DS/blob/main/Actividad_21/img/3.5.1.png)



se trabajaron el diagrama y el esquema



![ui](https://github.com/Jharvichu/Actividades_grupales_DS/blob/main/Actividad_21/img/3.5.2.png)



