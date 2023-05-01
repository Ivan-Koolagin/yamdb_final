import csv

from django.core.management.base import BaseCommand
from reviews.models import Category

PATH = "static/data/"


class Command(BaseCommand):
    help = "import data from category.csv"

    def handle(self, *args, **kwargs):
        with open(f"{PATH}/category.csv", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                print(row)

                category = Category(
                    id=row[0],
                    name=row[1],
                    slug=row[2],
                )
                category.save()
