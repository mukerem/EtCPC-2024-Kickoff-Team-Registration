from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib import messages
from django.forms import Form, CharField, ModelChoiceField
from django.db import IntegrityError
from django.db.models import Case, When, Value, IntegerField, F, Sum
from django.http import JsonResponse
from .models import Student, Team

def home(request):
    return render(request, 'home.html')

def student_list(request):
    query = request.GET.get('q')
    if query:
        students = Student.objects.filter(
            Q(name__icontains=query) | Q(email__icontains=query)
        ).order_by('name')
    else:
        students = Student.objects.all().order_by('name')
    registered_users = Student.objects.filter(is_registered=True).count()
    
    return render(request, 'student_list.html', {'students': students, 'registered_users': registered_users})

def register_student(request, student_id):
    student = Student.objects.get(id=student_id)
    if student.is_registered:
        messages.error(request, 'Student is already registered.')
    else:
        student.is_registered = True
        student.save()
        messages.success(request, 'Student registered successfully.')
    return redirect('student_list')

def unregister_student(request, student_id):
    student = Student.objects.get(id=student_id)
    student.is_registered = False
    student.save()
    messages.success(request, 'Student unregistered successfully.')
    return redirect('student_list')

def student_detail(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    return render(request, 'student_detail.html', {'student': student})

def team_list(request):
    query = request.GET.get('q', "")

    # Annotate each team with a calculated score
    teams = Team.objects.filter(
            name__icontains=query
        ).annotate(
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
    ).order_by('-team_score')
    return render(request, 'team_list.html', {'teams': teams})

class TeamRegistrationForm(Form):
    students = Student.objects.filter(is_registered=True).order_by("name")
    name = CharField(label='Team Name', max_length=100)
    member1 = ModelChoiceField(queryset=students, label='Member 1')
    member2 = ModelChoiceField(queryset=students, label='Member 2')
    member3 = ModelChoiceField(queryset=students, label='Member 3')

def register_team(request):
    if request.method == 'POST':
        form = TeamRegistrationForm(request.POST)
        if form.is_valid():
            try:
                # Create team and add members
                team = Team(name=form.cleaned_data['name'])
                team.save()
                team.members.add(form.cleaned_data['member1'], form.cleaned_data['member2'], form.cleaned_data['member3'])
                return redirect('team_detail', team_id=team.id)
            except IntegrityError:
                form.add_error('name', 'A team with this name already exists. Please choose a different name.')
    else:
        form = TeamRegistrationForm()
    return render(request, 'team_registration.html', {'form': form})
    
def team_detail(request, team_id):
    team = get_object_or_404(Team, pk=team_id)

    def get_score(score):
        return score if score > 0 else 0
    
    students = team.members.all()
    members_scores = [(member, get_score(member.leetcode_solved_problems_count), get_score(member.codeforces_solved_problems_count)) for member in team.members.all()]
    total_score = sum(score for _, score, _ in members_scores) + sum(score for _, _, score in members_scores)
    return render(request, 'team_detail.html', {'team': team, 'students': students, 'total_score': total_score})

def delete_team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)

    team.delete()
    messages.success(request, "Team deleted successfully.")
    return redirect('team_list')  # Redirect to the list of teams or some other appropriate page

def search_users(request):
    search_term = request.GET.get('term', '').strip()
    users = Student.objects.filter(
        Q(name__icontains=search_term) & Q(is_registered=True)
    ).order_by("name")

    results = [{'id': user.id, 'text': user.name} for user in users]
    return JsonResponse(results, safe=False)