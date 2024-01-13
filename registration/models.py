from django.db import models

class Student(models.Model):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female')]
    
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    leetcode_username = models.CharField(max_length=100)
    codeforces_username = models.CharField(max_length=100)
    leetcode_solved_problems_count = models.IntegerField(blank=True, null=True)
    codeforces_solved_problems_count = models.IntegerField(blank=True, null=True)
    is_registered = models.BooleanField(default=False)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    university = models.CharField(max_length=200, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    @property
    def leetcode_handle(self):
        leetcode_username = self.leetcode_username
        if "https://leetcode.com/" in leetcode_username:
            leetcode_username = leetcode_username.replace("https://leetcode.com/", "").replace("/", "")
        if "Leetcode.com/" in leetcode_username:
            leetcode_username = leetcode_username.replace("Leetcode.com/", "").replace("/", "")
        if "@" in leetcode_username:
            leetcode_username = leetcode_username.replace("@", "")
        
        return leetcode_username
    
    @property
    def codeforces_handle(self):
        codeforces_username = self.codeforces_username
        if "https://codeforces.com/profile/" in codeforces_username:
            codeforces_username = codeforces_username.replace("https://codeforces.com/profile/", "").replace("/", "")
        if "Codeforces.com/profile/" in codeforces_username:
            codeforces_username = codeforces_username.replace("Codeforces.com/profile/", "").replace("/", "")
        if "@" in codeforces_username:
            codeforces_username = codeforces_username.replace("@", "")
        return codeforces_username

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    members = models.ManyToManyField(Student, limit_choices_to={'is_registered': True})
    # Additional fields like created_at can be added if needed

    def __str__(self):
        return self.name

    @property
    def total_problems_solved(self):
        # Assuming you have a way to get problems solved from LeetCode and Codeforces
        # total = sum of problems solved by each member

        def get_score(score):
            return score if score > 0 else 0
        
        members_scores = [(member, get_score(member.leetcode_solved_problems_count), get_score(member.codeforces_solved_problems_count)) for member in self.members.all()]
        total_score = sum(score for _, score, _ in members_scores) + sum(score for _, _, score in members_scores)
        return total_score
    