import csv

from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404
from reviews.models import Genre, Title

PATH = "static/data/"


class Command(BaseCommand):
    help = "import data from genre_title.csv"

    def handle(self, *args, **kwargs):
        with open(f"{PATH}/genre_title.csv", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                print(row)
                title = get_object_or_404(Title, id=row[1])
                genre = get_object_or_404(Genre, id=row[2])
                title.save()
                title.genre.add(genre)
