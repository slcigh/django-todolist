from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from do.forms import TaskForm, ProjectForm, UserForm
from do.models import Task, Project
from django.http import Http404
from datetime import date, timedelta


@login_required(login_url='/do/register/')
def index(request):
    context_dict = {'project_list': Project.objects.filter(create_by=request.user)}
    if request.GET:
        context_dict['p_name'] = request.GET['p_name']
    if request.method == 'POST':
        form = ProjectForm(request.POST, request=request)
        if form.is_valid():
            t = form.save(commit=False)
            t.create_by = request.user
            t.save()
            return HttpResponseRedirect('/do/?p_name=' + t.slug)
    else:
        form = ProjectForm()
    context_dict['form'] = form
    context_dict['username'] = request.user
    return render(request, 'index.html', context_dict)


@login_required(login_url='/do/register/')
def task_filter(request):
    way = request.GET.get('way')
    context_dict = {}
    project_matrix = []
    project_list = Project.objects.filter(create_by=request.user)
    for project in project_list:
        unfinished_task = Task.objects.filter(project=project, is_finished=False)
        finished_task = Task.objects.filter(project=project, is_finished=True)
        if way == 'today':
            task_list = unfinished_task.filter(target_date=date.today())
            if task_list:
                project_matrix.append([project.name, task_list])
            context_dict['way'] = "Today's Task"
        if way == 'week':
            task_week = []
            for task in unfinished_task:
                if timedelta(0) <= (task.target_date - date.today()) <= timedelta(7):
                    task_week.append(task)
            if task_week:
                project_matrix.append([project.name, task_week])
            context_dict['way'] = "Next Week's Task"
        if way == 'finished':
            if finished_task:
                project_matrix.append([project.name, finished_task])
            context_dict['way'] = "Finished Task"
        if way == 'unfinished':
            if unfinished_task:
                project_matrix.append([project.name, unfinished_task])
            context_dict['way'] = "Unfinished Task"
        if way == 'overdue':
            task_overdue = []
            for task in unfinished_task:
                if task.target_date < date.today():
                    task_overdue.append(task)
            if task_overdue:
                project_matrix.append([project.name, task_overdue])
            context_dict['way'] = "Overdue Task"

    context_dict['project_dict'] = project_matrix
    return render(request, 'task_filter.html', context_dict)


@login_required(login_url='/do/register/')
def add_task(request, project_name):
    try:
        project = Project.objects.filter(create_by=request.user).get(slug=project_name)
    except Exception:
        raise Http404
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            return HttpResponseRedirect(request.GET['next'])
    else:
        form = TaskForm()
    task_list = Task.objects.filter(project=project)
    return render(request, 'show_task.html',
                  {'form': form, 'task_list': task_list, 'project_slug': project.slug, 'project_name': project.name})


@login_required(login_url='/do/register/')
def change_task_finish(request, project_name, task_id):
    project = Project.objects.get(slug=project_name, create_by=request.user)
    task = Task.objects.filter(project=project).get(id=task_id)
    if not task.is_finished:
        task.is_finished = True
        task.save()
    else:
        task.is_finished = False
        task.save()
    return HttpResponseRedirect(request.GET['next'])


@login_required(login_url='/do/register/')
def delete_task(request, project_name, task_id):
    project = Project.objects.get(slug=project_name, create_by=request.user)
    try:
        task = Task.objects.filter(project=project).get(id=task_id)
    except Exception:
        raise Http404
    if task:
        task.delete()
    return HttpResponseRedirect(request.GET['next'])


@login_required(login_url='/do/register/')
def edit_task(request):
    value = request.POST.get('value', '')
    pname_tid = request.POST.get('id', '')
    pname, tid = pname_tid.split("_")
    project = Project.objects.get(slug=pname, create_by=request.user)
    task = Task.objects.filter(project=project).get(id=int(tid))
    task.content = value
    task.save()
    return HttpResponse(value)


def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            for name in ['Personal', 'Work', 'Life', 'Reading']:
                try:
                    Project.objects.create_project(name=name, create_by=user)
                except Exception:
                    raise Http404
            new_user = authenticate(username=user_form.cleaned_data['username'],
                                    password=user_form.cleaned_data['password'], )
            login(request, new_user)
            return HttpResponseRedirect('/do/')
    else:
        user_form = UserForm()
    return render(request, 'login_register.html', {'form': user_form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect('/do/')
        else:
            return HttpResponseRedirect('/do/register/')


@login_required(login_url='/do/register/')
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/do/register/')
