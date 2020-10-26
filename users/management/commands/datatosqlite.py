import os
import uuid
import sqlite3

from api_yamdb.settings import BASE_DIR, DATABASES
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from category.models import Categories, Titles, Genres

User = get_user_model()


class Command(BaseCommand):

    def __custom_split(self, s):
        arr = s.split('"')
        string_replacement = {}
        for index in range(1, len(arr), 2):
            uid = str(uuid.uuid4())
            string_replacement[uid] = arr[index]
            arr[index] = uid

        s = '"'.join(arr)
        arr = [x.strip() for x in s.split(',')]
        for key in string_replacement:
            arr = [x.replace(key, string_replacement[key]) for x in arr]

        return arr

    def __import_table(self, obj_model, filename, new_names={}, related_keys={}):

        path_to_file = os.path.join(BASE_DIR, 'data', filename)
        with open(file=path_to_file, mode='r', encoding='utf-8') as f:

            names = [x.strip() for x in f.readline().split(',')]
            names = [new_names[x] if x in new_names else x for x in names]

            for line in f:
                values = self.__custom_split(line)
                properties = dict(zip(names, values))

                # Replace model_id with model object
                for key in properties:
                    if key in related_keys:
                        pk = int(properties[key])
                        model = related_keys[key]
                        obj = model.objects.filter(pk=pk).first()
                        properties[key] = obj

                try:
                    obj_model.objects.create(**properties)
                except Exception as e:
                    raise CommandError(f'Error during creation of model with properties {properties}. {e}')

    def __import_many_to_many_relations(self, filename, new_names={}):
        conn = None
        try:
            conn = sqlite3.connect(DATABASES['default']['NAME'])
        except Exception as e:
            print(e)

        cur = conn.cursor()
        cur.execute('DELETE FROM category_titles_genre;')
        conn.commit()

        path_to_file = os.path.join(BASE_DIR, 'data', filename)
        with open(file=path_to_file, mode='r', encoding='utf-8') as f:
            names = [x.strip() for x in f.readline().split(',')]
            names = [new_names[x] if x in new_names else x for x in names]
            names = ','.join(names)

            for line in f:
                line = line.strip()
                cur.execute(f'INSERT INTO category_titles_genre ({names}) VALUES ({line})')

            conn.commit()

        cur.close()
        conn.close()

        return conn

    def handle(self, *args, **options):

        try:
            User.objects.all().delete()
            Categories.objects.all().delete()
            Genres.objects.all().delete()
            Titles.objects.all().delete()

        except Exception as e:
            raise CommandError(f'Users table can not be cleaned. {e}')

        self.stdout.write(self.style.SUCCESS('Clean users table - OK'))

        User.objects.create_superuser(username='admin', email='admin@yamdb.fake', password='1234')
        self.stdout.write(self.style.SUCCESS('Create super user admin/admin@yamdb.fake/1234 - OK'))

        # IMPORT USERS.CSV
        self.__import_table(User, 'users.csv', {'description': 'bio'})
        self.stdout.write(self.style.SUCCESS('Import users.csv - OK'))

        # IMPORT CATEGORY.CSV
        self.__import_table(Categories, 'category.csv')
        self.stdout.write(self.style.SUCCESS('Import category.csv - OK'))

        # IMPORT GENRE.CSV
        self.__import_table(Genres, 'genre.csv')
        self.stdout.write(self.style.SUCCESS('Import genre.csv - OK'))

        # IMPORT TITLES.CSV
        self.__import_table(Titles, 'titles.csv', {}, {
            'category': Categories
        })
        self.stdout.write(self.style.SUCCESS('Import titles.csv - OK'))

        # IMPORT TITLE_GENRE RALATIONS GENRE_TITLE.CSV
        self.__import_many_to_many_relations('genre_title.csv', {
            'title_id': 'titles_id',
            'genre_id': 'genres_id'
        })
        self.stdout.write(self.style.SUCCESS('Import genre_title.csv - OK'))
