import csv
import os
import sqlite3

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from api_yamdb.settings import BASE_DIR, DATABASES

User = get_user_model()


class Command(BaseCommand):

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
            dr = csv.DictReader(f)

            for line in dr:
                names = list(line.keys())
                names = [new_names[x] if x in new_names else x for x in names]

                names += list(default_props.keys())
                questions = ['?']*len(names)

                names = ','.join(names)
                questions = ','.join(questions)

                values = list(line.values())
                values += list(default_props.values())
                values = [tuple(values)]
                cur.executemany(f'INSERT INTO {db_table_name} ({names}) VALUES ({questions});', values)

            conn.commit()

        cur.close()
        conn.close()

    def handle(self, *args, **options):

        # IMPORT USERS.CSV
        self.__import_table(
            filename='users.csv',
            db_table_name='api_myuser',
            new_names={'description': 'bio'},
            default_props={
                'password': '',
                'is_active': '1',
                'is_staff': '0',
                'is_superuser': '0',
                'date_joined': timezone.now()
            }
        )
        self.stdout.write(self.style.SUCCESS('Import users.csv - OK'))

        # CREATE SUPER USER
        User.objects.create_superuser(username='admin', email='admin@yamdb.fake', password='1234')
        self.stdout.write(self.style.SUCCESS('Create super user admin/admin@yamdb.fake/1234 - OK'))

        # IMPORT CATEGORY.CSV
        self.__import_table(
            filename='category.csv',
            db_table_name='api_category',
        )

        self.stdout.write(self.style.SUCCESS('Import category.csv - OK'))

        # IMPORT GENRE.CSV
        self.__import_table(
            filename='genre.csv',
            db_table_name='api_genre',
        )
        self.stdout.write(self.style.SUCCESS('Import genre.csv - OK'))

        # IMPORT TITLES.CSV
        self.__import_table(
            filename='titles.csv',
            db_table_name='api_title',
            new_names={'category': 'category_id'},
            default_props={'description': ''}
        )
        self.stdout.write(self.style.SUCCESS('Import titles.csv - OK'))

        # IMPORT TITLE_GENRE RELATIONS GENRE_TITLE.CSV
        self.__import_table(
            filename='genre_title.csv',
            db_table_name='api_title_genre',
        )
        self.stdout.write(self.style.SUCCESS('Import genre_title.csv - OK'))

        # IMPORT REVIEW.CSV
        self.__import_table(
            filename='review.csv',
            db_table_name='api_review',
            new_names={'author': 'author_id'}
        )
        self.stdout.write(self.style.SUCCESS('Import review.csv - OK'))

        # IMPORT COMMENT.CSV
        self.__import_table(
            filename='comments.csv',
            db_table_name='api_comment',
            new_names={'author': 'author_id'}
        )
        self.stdout.write(self.style.SUCCESS('Import comments.csv - OK'))
