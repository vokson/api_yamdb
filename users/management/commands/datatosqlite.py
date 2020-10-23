from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from api_yamdb.settings import BASE_DIR
import os

User = get_user_model()


class Command(BaseCommand):

    def __import_table(self, obj_model, filename, new_names):

        path_to_file = os.path.join(BASE_DIR, 'data', filename)
        with open(path_to_file, 'r') as f:

            names = [x.strip() for x in f.readline().split(',')]
            names = [new_names[x] if x in new_names else x for x in names]

            for line in f:
                values = [x.strip() for x in line.split(',')]
                properties = dict(zip(names, values))

                try:
                    User.objects.create(**properties)
                except Exception as e:
                    raise CommandError(f'Error during creation of model with properties {properties}. {e}')

    def handle(self, *args, **options):
        try:
            User.objects.all().delete()

        except Exception as e:
            raise CommandError(f'Users table can not be cleaned. {e}')

        self.stdout.write(self.style.SUCCESS('Clean users table - OK'))

        User.objects.create_superuser(username='admin', email='admin@yamdb.fake', password='1234')
        self.stdout.write(self.style.SUCCESS('Create super user admin/admin@yamdb.fake/1234 - OK'))

        # IMPORT USERS.CSV
        self.__import_table(User, 'users.csv', {'description': 'bio'})
        self.stdout.write(self.style.SUCCESS('Import users.csv - OK'))
