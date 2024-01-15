import csv
from django.core.management.base import BaseCommand
from registration.models import Student, Team
from registration.utils import username_adjust

class Command(BaseCommand):
    help = 'Fetch leetcode and codeforces solved problems count'

    def handle(self, *args, **options):

        # Open or create a CSV file
        with open('students.csv', 'w', newline='') as csvfile:
            # Define the CSV writer
            fieldnames = ['Name', 'Email', 'Phone Number',  'Leetcode Username', 'Codeforces Username', 'Leetcode Solved Problems Count', 'Codeforces Solved Problems Count', 'Gender', 'Age', 'University', 'Department', 'Team']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write the header
            writer.writeheader()

            # Query students who are part of a team
            students = Student.objects.filter(team__isnull=False).distinct()

            # Write student data
            for student in students:
                # Get the team name (assuming only one team per student)
                team_name = student.team_set.first().name if student.team_set.exists() else ''
                leetcode_username, codeforces_username = username_adjust(student)

                # Write row for each student
                writer.writerow({
                    'Name': student.name,
                    'Email': student.email,
                    'Phone Number': student.phone_number,
                    'Leetcode Username': leetcode_username if student.leetcode_solved_problems_count >= 0 else None,
                    'Codeforces Username': codeforces_username if student.codeforces_solved_problems_count >= 0 else None,
                    'Leetcode Solved Problems Count': student.leetcode_solved_problems_count,
                    'Codeforces Solved Problems Count': student.codeforces_solved_problems_count,
                    'Gender': student.gender,
                    'Age': student.age,
                    'University': student.university,
                    'Department': student.department,
                    'Team': team_name
                })