# Proyecto de grado

## Dependencias

- Python 3.11.1
- Django 4.1.6
- PostgreSQL 15.1
- Docker 4.16.1
<!-- - Redis 7.0.8 -->

## Comandos

### Ejecutar el proyecto

```bash
python src/manage.py runserver 0:8000
```

### Crear migraciones

```bash
python src/manage.py makemigrations <app>
```

> `<app>` es el nombre de la aplicación

### Ejecutar las migraciones

```bash
python src/manage.py migrate <app>
```

> `<app>` es el nombre de la aplicación
>
> `--fake` asegura que se ejecute la última versión y salte las migraciones faltantes

### Docker

#### Ejecutar CLI

```bash
docker exec -it [container_name] bash
docker exec -it [container_name] sh
```

#### Crear y ejecutar contenedores con Logs

```bash
docker-compose up --build
```

#### Crear y ejecutar contenedores sin Logs

```bash
docker-compose up --build -d
```

#### Detener los contenedores

```bash
docker-compose stop
```

#### Detener y eliminar los contenedores

```bash
docker-compose down
```

## Estructura de carpetas

```bash
.
├──src······················#Código fuente del proyecto
├──.gitignore···············#Carpetas y Archivos que serán ignorados por GIT
├──docker-compose.yml·······#Archivo de configuración de Docker Compose
├──Dockerfile···············#Archivo de configuración de Docker
├──requirements.md··········#Lista de las dependencias del proyecto
└──README.md················#Documentación útil para el desarrollo del proyecto
```

```bash
.src 
├──app······················#Aplicaciones del proyecto
├──core·····················#Núcleo de las aplicaciones
├──home·····················#Aplicación de inicio
├──jobboard·················#Sitio web del projecto
├──media····················#Carpeta para el almacenamiento de archivos multimedia
├──users····················#Aplicación de usuarios (sistema de usuarios)
└──manage.py················#Archivo principal de Django
```

## Manual para ejecutar el proyecto desde el principio

### Sin Docker

1. Descargue `Python 3.11.1`
2. Descargue `PostgreSQL 15.1`
3. Cree una base de datos en PostgreSQL llamada `db_job`
4. Clone el repositorio

   ```bash
   git clone https://github.com/jotaprogramming/bolsaempleo2023.git
   ```

5. Ingrese a la raíz del proyecto
6. Instale un entorno virtual para Python

   > En nuestro caso usamos `VirtualEnv`

   1. Instalar `VirtualEnv`

      ```bash
      pip install virtualenv
      ```

   2. Crear entorno virtual

      ```bash
      virtualenv env
      ```

   3. Activar entorno virtual
      - En Windows

        ```bash
        .\env\Scripts\activate
        ```

      - En Linux

        ```bash
        source env/bin/activate
        ```

7. Instale las dependencias del proyecto

   ```bash
   pip install -r requirements.txt
   ```

8. Solicite el archivo de configuraciones de las variables de entorno

9. Asegúrese que el servidor de PostgreSQL esté funcionando y ejecute las migraciones

   ```bash
   python src/manage.py makemigrations
   ```

   ```bash
   python src/manage.py migrate
   ```

10. Levante el servidor de Django

    ```bash
    python src/manage.py runserver 0:8000
    ```

### Con Docker

1. Ejecute Docker Compose

   ```bash
   docker-compose up --build -d
   ```

2. Ejecute las migraciones

   ```bash
   docker exec -it <web_container_name> python manage.py makemigrations
   ```

   ```bash
   docker exec -it <web_container_name> python manage.py migrate
   ```

   > PD: para ver el nombre del contenedor llamado `web`, ejecute `docker ps`
