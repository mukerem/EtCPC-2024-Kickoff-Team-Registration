import csv
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError 
from registration.models import Student

class Command(BaseCommand):
    help = 'Imports students from a CSV file'

    # def add_arguments(self, parser):
    #     parser.add_argument('csv_file', type=str, help='The CSV file to import')

    def handle(self, *args, **options):
        # file_path = options['csv_file']
        file_path = "registration/management/commands/data.csv"

        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    try:
                        Student.objects.get_or_create(
                            name=row['Full Name'],
                            email=row['Email'],
                            phone_number=row.get('Phone Number'),
                            gender=row.get('gender'),
                            age=row.get('Age'),
                            university=row.get('University/College/School Name'),
                            department=row.get('Department', ''),
                            leetcode_username=row['⁠LeetCode Username'],
                            codeforces_username=row['Codeforces Username']
                        )
                    except IntegrityError as e:
                        # print(row['Full Name'])
                        print(e)

            self.stdout.write(self.style.SUCCESS('Successfully imported students'))
        except FileNotFoundError:
            raise CommandError('File "%s" does not exist' % file_path)

