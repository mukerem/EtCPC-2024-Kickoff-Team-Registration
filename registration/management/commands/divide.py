import json
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError 
from registration.models import Student, Team
from registration.utils import username_adjust
from registration.stats import leetcode_solved_problems, codeforces_solved_problems
from django.db.models import Case, When, Value, IntegerField, F, Sum


class Command(BaseCommand):
    help = 'Fetch leetcode and codeforces solved problems count'

    def handle(self, *args, **options):

        teams = Team.objects.annotate(
        team_score=Sum(
            Case(
                When(members__leetcode_solved_problems_count__gt=0, then=F('members__leetcode_solved_problems_count')),
                default=Value(0),
                output_field=IntegerField()
            ) +
            Case(
                When(members__codeforces_solved_problems_count__gt=0, then=F('members__codeforces_solved_problems_count')),
                default=Value(0),
                output_field=IntegerField()
            )
        )
        ).filter(team_score__lt=475)
        user_name = []
        for i in teams:
            members = i.members.all()
            for member in members:
                leetcode_username, codeforces_username = username_adjust(member)
                # if member.leetcode_solved_problems_count >= 0:
                #     user_name.append(leetcode_username)
                if member.codeforces_solved_problems_count >= 0:
                    user_name.append(codeforces_username)
        
    
        with open("division1.json", "w") as f:
            json.dump(user_name, f, indent=4)

        for i in user_name:
            print(i)