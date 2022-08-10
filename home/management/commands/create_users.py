from users.models import User
from django.core.management.base import BaseCommand, CommandError
import csv



class Command(BaseCommand):
    """
    Base command used for importing customers in a CSV file.
    This file must contain the columns:
     "first_name", "last_name", "email", "gender", "company", "city", "title", "latitude", "longitude"
    """
    help = "Imports a .csv file with customers' names and inserts them into database."

    def add_arguments(self, parser):
        parser.add_argument('file', type=str, help='CSV File name (Ex.: users.csv).')

    def handle(self, *args, **options):
        filename = options['file']
        if not filename:
            raise CommandError('No file was specified.')
        errors = False
        #users = []
        count=0

        with open(filename, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=',')
            try:
                for row in reader:
                    #print(f'Id to be imported:{row["Username"]}')
                    try:
                        User.objects.get(username=row['Username'])
                    except User.DoesNotExist:
                        User.objects.create_user(username=row['Username'],password=row['Password'])
                        count=count+1
                        
            except Exception as e:#KeyError:
                # File structure is incorrect, its first column must be "name".
                print(e)
                errors = True
        if errors:
            self.stdout.write(self.style.ERROR('File has incorrect format. It''s missing a "Username" column.'))
            return
        #created = User.objects.bulk_create(users, ignore_conflicts=False)
        #count = len(created)
        if count==0:
            self.stdout.write(self.style.WARNING('File was imported but no customer was registered.'))
            return
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully imported Users file and registered {count} '
                f'customer{"s" if count != 1 else ""}. '
            )
        )

