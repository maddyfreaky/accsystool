from django.urls import reverse
import re 
from django.utils.timesince import timesince
from django.http import JsonResponse
from django.utils.dateformat import format
from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    # path('task_management/',views.task_management,name='task_management'),
    path('todopgt/', views.todopgt, name='todopgt'),    
    path('projects/<int:project_id>/', views.projects, name='projects'),
    path('projects/<int:project_id>/create_issue/', views.create_issue, name='create_issue'),
    path('issue/edit/<int:issue_id>/', views.edit_issue, name='edit_issue'),

    path('issue/delete/<int:issue_id>/', views.delete_issue, name='delete_issue'),

    # path('register/', views.register, name='register'),  # URL for the register page
    # path('', views.user_login, name='login'),
    # path('logout/', views.user_logout, name='logout'),  # URL for the logout view
    path('projects/<int:project_id>/create-todolist/', views.create_todolist, name='create_todolist'),
    path('api/projects/all/', views.fetch_all_data, name='fetch_all_data'),
    path('todlistpage/', views.todlistpage, name='todlistpage'),
    path('delete_project/<int:project_id>/', views.delete_project, name='delete_project'),
    path('todotable/', views.todotable, name='todotable'),
    path('user_list/', views.user_list, name='user_list'),
    path('user-project/<int:user_id>/', views.user_project, name='user_project'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('user-project/<int:user_id>/create/', views.create_project, name='create_project'),
]