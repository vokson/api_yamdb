import os
import sqlite3
import uuid

from api_yamdb.settings import BASE_DIR, DATABASES
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

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

    def __import_table(self, filename, db_table_name, new_names={}, default_props={}):
        conn = None
        try:
            conn = sqlite3.connect(DATABASES['default']['NAME'])
        except Exception as e:
            print(e)

        cur = conn.cursor()
        cur.execute(f'DELETE FROM {db_table_name}')
        conn.commit()

        path_to_file = os.path.join(BASE_DIR, 'data', filename)
        with open(file=path_to_file, mode='r', encoding='utf-8') as f:
            names = [x.strip() for x in f.readline().split(',')]
            names = [new_names[x] if x in new_names else x for x in names]
            names += default_props.keys()
            names = ','.join(names)

            for line in f:
                values = self.__custom_split(line)
                values += default_props.values()
                values = [x.strip('"') for x in values]
                values = ','.join([f'"{x}"' for x in values])
                cur.execute(f'INSERT INTO {db_table_name} ({names}) VALUES ({values})')

            conn.commit()

        cur.close()
        conn.close()

    def handle(self, *args, **options):

        # IMPORT USERS.CSV
        # self.__import_table(User, 'users.csv', {'description': 'bio'})
        self.__import_table(
            filename='users.csv',
            db_table_name='users_myuser',
            new_names={'description': 'bio'},
            default_props={
                'password': '',
                'confirmation_code': '',
                'is_active': '1',
                'is_admin': '0'
            }
        )
        self.stdout.write(self.style.SUCCESS('Import users.csv - OK'))

        # IMPORT CATEGORY.CSV
        self.__import_table(
            filename='category.csv',
            db_table_name='category_categories',
        )
        self.stdout.write(self.style.SUCCESS('Import category.csv - OK'))

        # IMPORT GENRE.CSV
        self.__import_table(
            filename='genre.csv',
            db_table_name='category_genres',
        )
        self.stdout.write(self.style.SUCCESS('Import genre.csv - OK'))

        # IMPORT TITLES.CSV
        self.__import_table(
            filename='titles.csv',
            db_table_name='category_titles',
            new_names={'category': 'category_id'},
            default_props={'description': ''}
        )
        self.stdout.write(self.style.SUCCESS('Import titles.csv - OK'))

        # IMPORT TITLE_GENRE RELATIONS GENRE_TITLE.CSV
        self.__import_table(
            filename='genre_title.csv',
            db_table_name='category_titles_genre',
            new_names={
                'title_id': 'titles_id',
                'genre_id': 'genres_id'
            }
        )
        self.stdout.write(self.style.SUCCESS('Import genre_title.csv - OK'))

        # CREATE SUPER USER
        User.objects.create_superuser(username='admin', email='admin@yamdb.fake', password='1234')
        self.stdout.write(self.style.SUCCESS('Create super user admin/admin@yamdb.fake/1234 - OK'))
