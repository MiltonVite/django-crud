from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Task, Project
from .forms import CreateNewTask, createNewProjetc
# Create your views here.

def hello(request, username):
    print(username)
    return HttpResponse("<h1>Hello World %s</h1>" % username)

def about(request):
    username = "Milton"
    return render(request, 'about.html', {"username": username})

def indez(request):
    title = "Welcome to the Home Page!!"
    return render(request, 'index.html', {"title": title})

def project(request):
    #projects = list(Project.objects.values())
    projects = Project.objects.all()
    return render(request, "projects/project.html", {"projects": projects})

def task(request):
    #task = Task.objects.get(title=title)
    #task =get_object_or_404(Task, name=name)
    tasks = Task.objects.all()
    return render(request, "tasks/task.html",  {"tasks": tasks})

def create_task(request):
    if request.method == 'GET':
        return render(request, "tasks/create_task.html", {
            'form': CreateNewTask()
        })
    else:
        Task.objects.create(title=request.POST['title'], description=request.POST['description'], project_id=1)
        return redirect('task')
    # Task.objects.create(title=request.GET['title'], description=request.GET['description'], project_id=1)
    # return render(request, "create_task.html", {
    #     'form': CreateNewTask()
    # })

def create_project(request):
    if request.method == 'GET':
        return render(request, "projects/create_projects.html", {
            'form': createNewProjetc()
        })
    else:
        Project.objects.create(name=request.POST['name'])
        return redirect('project')
    
def project_detail(request, id):
    # project = Project.objects.get(id=id)
    project = get_object_or_404(Project, id=id)
    tastks = Task.objects.filter(project_id=id)
    return render(request, "projects/detail.html", {"project": project,
                                                    "tasks": tastks}) 