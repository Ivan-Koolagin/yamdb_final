import csv

from django.core.management.base import BaseCommand
from reviews.models import User

PATH = "static/data/"


class Command(BaseCommand):
    help = 'import data from users.csv'

    def handle(self, *args, **kwargs):
        with open(f'{PATH}/users.csv', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)

            User.objects.all().delete()

            for row in reader:
                print(row)

                user = User(
                    id=row[0],
                    username=row[1],
                    email=row[2],
                    role=row[3],
                    bio=row[4],
                    first_name=row[5],
                    last_name=row[6]
                )
                user.save()
