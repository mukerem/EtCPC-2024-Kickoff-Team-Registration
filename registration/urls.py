from django.urls import path

from registration.views import *

urlpatterns = [
    path('', home, name='home'),
    path("student/list/", student_list, name="student_list"),
    path("student/register/<int:student_id>/", register_student, name="register_student"),
    path("student/unregister/<int:student_id>/", unregister_student, name="unregister_student"),
    path('students/<int:student_id>/', student_detail, name='student_detail'),
    path('team/register/', register_team, name='register_team'),
    path('team/list/', team_list, name='team_list'),
    path('team/detail/<int:team_id>/', team_detail, name='team_detail'),
    path('team/delete/<int:team_id>/', delete_team, name='delete_team'),
    path('team/search', search_users, name='search_users'),

]
