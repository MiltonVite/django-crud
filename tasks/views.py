from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from .form import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required


# Create your views here.

def home(request):
    return render(request, 'home.html', {'form': UserCreationForm})

def singup(request):
    if request.method == 'GET':
        return render(request, 'singup.html', {'form': UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            #register user
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('task')
                #return render(request, 'singup.html', {'form': UserCreationForm, 'error': 'User created successfully'})
            except IntegrityError:
                return render(request, 'singup.html', {'form': UserCreationForm, 'error': 'Username already exists'})
        return render(request, 'singup.html', {'form': UserCreationForm, 'error': 'Passwords did not match'})

@login_required
def task(request):
    task = Task.objects.filter(user=request.user , datecomplete__isnull=True) 
    return render(request, 'task.html', {'task': task })

def singout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {'form': AuthenticationForm})
    else:
        print(request.POST)
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {'form': AuthenticationForm, 'error': 'Username and password did not match'})
        else:
            login(request, user)
            return redirect('task')
        #return render(request, 'signin.html', {'form': AuthenticationForm})

@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {'form': TaskForm})
    else:
        #print(request.POST)
        try:
            formulario = TaskForm(request.POST)
            new_task=formulario.save(commit=False)
            new_task.user = request.user
            new_task.save()
            print(formulario)
            print(new_task)
            return redirect('task')
        except ValueError:
            return render(request, 'create_task.html', {'form': TaskForm, 'error': 'Por favor, verifique los datos ingresados'})
        
@login_required
def task_datail(request, task_id):
    if request.method == 'GET':
        print(task_id)
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_datail.html', {'task': task , 'form': form}) 
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('task')
        except ValueError:
            return render(request, 'task_datail.html', {'task': task , 'form': form, 'error': 'Por favor, verifique los datos ingresados'})

@login_required
def task_complete(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecomplete = timezone.now()
        task.save()
        return redirect('task')

@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task')
@login_required
def task_completed(request):
    task = Task.objects.filter(user=request.user , datecomplete__isnull=False).order_by('-datecomplete')
    return render(request, 'task.html', {'task': task })