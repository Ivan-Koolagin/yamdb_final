# yamdb_final

![example workflow](https://github.com/Ivan-Koolagin/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

====
REST API проект для сервиса YaMDb — сбор отзывов о фильмах, книгах или музыке.

## Стек технологий:
- Python3
- Django
- Django REST
- Gunicorn
- nginx
- Docker
- Docker compose
- Yandex Cloud
- PostgreSQL
- GIT

## Описание

Проект **YaMDb** собирает отзывы пользователей (Review) на произведения (Titles). 
Произведения делятся на категории: «Книги», «Фильмы», «Музыка». 
Список категорий (Category) может быть расширен администратором 
(например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).

### Запуск проекта:

Находясь в корне проекта ереходим в директорию с docker-compose.yaml:
```bash
cd infra
```

Запускаем контейнеры (infra_db_1, infra_web_1, infra_nginx_1):
```bash
docker compose up -d --build
```

Выполняем миграции:

```bash
docker-compose exec web python manage.py migrate
```

Создаем суперпользователя:
```bash
docker-compose exec web python manage.py createsuperuser
```

Србираем статику:
```bash
docker-compose exec web python manage.py collectstatic --no-input
```

Создаем дамп базы данных (в отдельном репозитории):
```bash
docker-compose exec web python manage.py dumpdata  --exclude auth.permission --exclude contenttypes > fixtures.json
```

Для выгрузки данных из дампа в БД:
```bash
cat fixtures.json | sudo docker exec -i <<container_name_or_id>> python manage.py loaddata --format=json -
```

Останавливаем контейнеры:
```bash
docker-compose down -v
```

### Документация API YaMDb
Документация доступна по эндпойнту: http://localhost/redoc/

### Работу выполнил:
[Кулагин Иван](https://github.com/Ivan-Koolagin) - Email - ```ivkulagin@gmail.com```

