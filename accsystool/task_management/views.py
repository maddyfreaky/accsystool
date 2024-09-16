from django.http import JsonResponse
from django.utils.dateformat import format
from django.utils import timezone
from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.timesince import timesince
from django.views.decorators.http import require_POST
from django.urls import reverse
import re
from django.contrib import messages
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse



# Create your views here.

# def task_management(request):
#     return render(request,'task_management.html')
@login_required
def todlistpage(request):
    # Retrieve all projects, ordered by creation time (most recent first)
    projects = Project.objects.all().order_by('-created_at')
    return render(request, 'todopage.html', {'projects': projects})

def todopgt(request):
     if request.method == 'POST':
        projectname = request.POST.get('projectname')
        print(projectname)
        if projectname:
            # Create and save the project
            Project.objects.create(projectname=projectname)
            return redirect('todlistpage')  # Redirect to the project list page after saving
     return render(request,"todolist.html")

@login_required
def projects(request, project_id):
    print("pross")
    project = get_object_or_404(Project, id=project_id)
    print(project,"Project name")
    issues = project.issues.all()  # Retrieve all issues related to the project

    todotask = project.details.filter(user=request.user)  # Filter issues by the current user

    

   # Combine project details and comments into one list
    combined_list = list(todotask)

    # Sort by creation date
    combined_list.sort(key=lambda x: x.created_at, reverse=True)
    
    # Calculate time ago
    for item in combined_list:
        item.time_ago = timesince(item.created_at).split(', ')[-1]  # Time ago (e.g., "1 hour")

    # Perform actions related to the specific project
    return render(request, 'todolist.html', {'project': project,"issues":issues,"todotask":todotask})

def create_issue(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    if request.method == 'POST':
        issuename = request.POST.get('issuename')
        print(issuename)
        if issuename:
            print("if",issuename)
            Issue.objects.create(project=project, title=issuename, description=issuename)
            return redirect('projects', project_id=project.id)
    
    return render(request, 'todolist.html', {'project': project})

def edit_issue(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)
    
    if request.method == 'POST':
        issue.description = request.POST.get('description')
        issue.save()
        
        return redirect('projects', project_id=issue.project.id)  # Redirect to the project's issues view

    return render(request, 'edit_issue.html', {'issue': issue})

@require_POST
def delete_issue(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)
    project_id = issue.project.id  # Capture the project ID before deleting
    issue.delete()
    return redirect('projects', project_id=project_id)  # Redirect to the projects view after deletion

@login_required
def create_todolist(request, project_id):
    print("Entered create_todolist view")
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        print("POST method detected")
        description = request.POST.get('description')
        comments = request.POST.get('comments')
        attached_file = request.FILES.get('attached_file')

        print(f"Description: {description}")
        print(f"Comments: {comments}")
        print(f"Attached File: {attached_file}")

        if description:
            # Save the data to the database
            todolist = Todolist(
                project=project,
                description=description,
                comments=comments,
                attached_file=attached_file,
                user=request.user  # Set the user to the current logged-in user

            )
            todolist.save()
            print("new Data saved successfully")

            return redirect('projects', project_id=project.id)
        else:
            print("No description provided")

    return render(request, 'todolist.html', {'project': project})

def fetch_all_data(request):
    print("fetching all data")

    # Fetch all projects and tasks
    projects = Project.objects.all()
    todotasks = Todolist.objects.all()

    # Serialize project data
    data = []
    for project in projects:
        data.append({
            'id': project.id,
            'title': f"Project: {project.projectname}",  # Ensure projectname is the correct field
            'created_at': format(project.created_at, 'Y-m-dTH:i:sZ'),
        })

    # Serialize task data
    for task in todotasks:
        data.append({
            'id': task.id,
            'title': f"Comment for {task.project.projectname}",  # Use the correct field name
            'created_at': format(task.created_at, 'Y-m-dTH:i:sZ'),
            'description': task.description,  # Include the description field if needed
        })

    return JsonResponse(data, safe=False)

def todolist(request):
    print("todo")
    return render(request,"todolist.html")

def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    project.delete()
    messages.success(request, 'Project deleted successfully.')
    return redirect('todlistpage')  # Redirect to your project list view after deletion

@require_POST
def update_issue(request, issue_id):
    data = json.loads(request.body)
    try:
        issue = Issue.objects.get(pk=issue_id)
        issue.status = data['status']
        issue.updated_at = timezone.now()  # Update the timestamp
        issue.save()
        return JsonResponse({'success': True, 'message': 'Issue updated successfully'})
    except Issue.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Issue not found'}, status=404)


def todotable(request):
    project1 = Todolist.objects.all()
    print(project1,"this is test")
    return render(request,"todotable.html",{"project1":project1})

@login_required
def user_list(request):
    if request.user.is_superuser:  # Check if the logged-in user is an admin (superuser)
        users = User.objects.exclude(is_superuser=True).exclude(id=request.user.id)
        return render(request, 'user_list.html', {'users': users})
    else:
        # Redirect non-superusers or show a permission denied message
        return JsonResponse({'error': 'Permission Denied'}, status=403)

def user_project(request, user_id):
    print("user_project function")
    # Get the user by ID or return 404 if not found
    user = get_object_or_404(User, id=user_id)

    # Get all projects associated with the specific user
    user_projects = Project.objects.filter(user=user).order_by('-created_at')
    print("this is the user_projects",user_projects)
    context = {
        'user': user,  # Pass the selected user
        'projects': user_projects,  # Pass the projects for this user
    }

    return render(request, 'user_project.html', context)

@login_required
def delete_user(request, user_id):
    if request.user.is_superuser:
        user = get_object_or_404(User, id=user_id)
        user.delete()
        return JsonResponse({'success': 'User deleted successfully.'})  # Return JSON response on successful deletion
    else:
        return JsonResponse({'error': 'Permission Denied'}, status=403)  # Return error response if user is not superuser

def create_project(request, user_id):
    print("create pgt function")
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        # Get form data from POST request
        projectname = request.POST.get('projectname')
        taskname = request.POST.get('taskname')
        priority = request.POST.get('priority')
        from_date = request.POST.get('fromdate')
        to_date = request.POST.get('todate')

        try:
            print("try block")
            # Create and save new Project instance, linking it to the user
            project = Project(
                projectname=projectname,
                taskname=taskname,
                priority=priority,
                from_date=from_date,
                to_date=to_date,
                user=user,  # Associate the project with the selected user
                assigned_by=request.user  # Set the user creating the project

            )
            project.save()
            print(" project data saved")

            # Redirect back to the user's project page
            return redirect('user_project', user_id=user.id)

        except Exception as e:
            print("except")
            return HttpResponse(f"An error occurred: {e}", status=500)

    # If GET request, just render the page with the user's existing projects
    projects = Project.objects.filter(user=user)
    return render(request, 'userproject.html', {'projects': projects, 'user': user})