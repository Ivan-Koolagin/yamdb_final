import csv
import os
from api_yamdb.settings import BASE_DIR
from typing import List

from django.core.management import BaseCommand, CommandError
from django.shortcuts import get_object_or_404
from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from users.models import User


CSV_FILES = (
    ("users.csv", User),
    ("category.csv", Category),
    ("genre.csv", Genre),
    ("titles.csv", Title),
    ("review.csv", Review),
    ("comments.csv", Comment),
    ("genre_title.csv", GenreTitle),
)
FOREIGN_FIELD_NAMES = {
    "review": Review,
    "author": User,
    "title": Title,
    "genre": Genre,
    "category": Category,
    "genre_title": GenreTitle,
}


def check_fields(fields_name: List[str], model_fields: List[str]):
    for i, _ in enumerate(fields_name):
        fields_name[i] = fields_name[i].lower()
        fields_name[i] = fields_name[i].replace("_id", "")
        if not fields_name[i] in model_fields:
            raise CommandError(
                f"{fields_name[i]} field doesn't exist " "in {Model} Model"
            )


def save_model(model, row, fields_name):
    try:
        obj = model()
        for i, field in enumerate(row):
            if fields_name[i] in FOREIGN_FIELD_NAMES.keys():
                foreign_model = FOREIGN_FIELD_NAMES[fields_name[i]]
                field = get_object_or_404(foreign_model, id=field)
            setattr(obj, fields_name[i], field)
        obj.save()
    except Exception as e:
        raise CommandError(e)


def process_file(csv_file, model):
    path = os.path.join(BASE_DIR, f"static/data/{csv_file}")
    model_fields = [f.name for f in model._meta.fields]
    with open(path, "rt", encoding="utf8") as f:
        reader = csv.reader(f, dialect="excel")
        fields_name = next(reader)
        check_fields(fields_name, model_fields)
        for row in reader:
            save_model(model, row, fields_name)


def process_genre_title():
    with open(
        os.path.join(BASE_DIR, "static/data/genre_title.csv"), "rt", encoding="utf8"
    ) as f:
        reader = csv.reader(f, dialect="excel")
        next(reader)
        for row in reader:
            try:
                title = get_object_or_404(Title, id=int(row[1]))
                genre = get_object_or_404(Genre, id=int(row[2]))
                title.genre.add(genre)
                title.save()
            except Exception as e:
                raise CommandError(e)


class Command(BaseCommand):
    help = "Load csv files into the database"

    def handle(self, *args, **options):
        for csv_file, model in CSV_FILES:
            process_file(csv_file, model)
        process_genre_title()
