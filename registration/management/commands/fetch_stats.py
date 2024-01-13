from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError 
from registration.models import Student
from registration.stats import leetcode_solved_problems, codeforces_solved_problems
class Command(BaseCommand):
    help = 'Fetch leetcode and codeforces solved problems count'

    def handle(self, *args, **options):

        students = Student.objects.all()
        x = False
        for student in students:
            if student.leetcode_solved_problems_count is not None:
                continue
            codeforces_username = student.codeforces_username
            if "https://codeforces.com/profile/" in codeforces_username:
                codeforces_username = codeforces_username.replace("https://codeforces.com/profile/", "").replace("/", "")
            if "Codeforces.com/profile/" in codeforces_username:
                codeforces_username = codeforces_username.replace("Codeforces.com/profile/", "").replace("/", "")
            if "@" in codeforces_username:
                codeforces_username = codeforces_username.replace("@", "")

            leetcode_username = student.leetcode_username
            if "https://leetcode.com/" in leetcode_username:
                leetcode_username = leetcode_username.replace("https://leetcode.com/", "").replace("/", "")
            if "Leetcode.com/" in leetcode_username:
                leetcode_username = leetcode_username.replace("Leetcode.com/", "").replace("/", "")
            if "@" in leetcode_username:
                leetcode_username = leetcode_username.replace("@", "")
            
            leetcode_solved_problems_count = leetcode_solved_problems(leetcode_username)
            codeforces_solved_problems_count = codeforces_solved_problems(codeforces_username)
            student.leetcode_solved_problems_count = leetcode_solved_problems_count
            student.codeforces_solved_problems_count = codeforces_solved_problems_count
            student.save()
            print(student.name, leetcode_solved_problems_count, codeforces_solved_problems_count)
# >>> a = Student.objects.filter(leetcode_solved_problems_count__isnull=True)