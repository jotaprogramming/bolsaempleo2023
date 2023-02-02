# Proyecto de grado

## Dependencies

- Python 3.11.1
- Django 4.1.6
- PostgreSQL 15.1
- Redis 7.0.8
- Docker 4.16.1

## Commands

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

### Docker Compose

#### Crear y ejecutar imágenes Docker con Logs

```bash
docker-compose up --build
```

#### Crear y ejecutar imágenes Docker sin Logs

```bash
docker-compose up --build -d
```

#### Detener la red y los contenedores

```bash
docker-compose stop
```

#### Detener y eliminar la red y los contenedores

```bash
docker-compose down
```
