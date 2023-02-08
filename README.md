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
