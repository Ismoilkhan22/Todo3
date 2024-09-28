from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from base.helper import permission_check, user_home

from core.forms.task import TaskForm
from core.models.task import Task


@login_required(login_url='login')
def task_filter(request, key, pk):
    root = Task.objects.filter(id=pk).first()
    if not root:
        return render(request, 'base.html', {"error": 404})

    task = Task.objects.filter(**{key: root})
    paginator = Paginator(task, 15)
    page = request.GET.get('page', 1)
    result = paginator.get_page(page)

    ctx = user_home(request)
    ctx['task'] = result
    ctx['root'] = root

    return render(request, 'pages/user_home.html', ctx)


@login_required(login_url='login')
def manage_task(request, pk=None, delete=0, status=None):
    root = None
    user = request.user
    if pk:
        root = Task.objects.filter(pk=pk, user=user).first()
        if delete:
            root.delete()
            return redirect('task')
    form = TaskForm(request.POST or None, request.FILES or None,   instance=root)
    if form.is_valid():
        task = form.save(commit=False)
        task.user = request.user
        task.save()
        print('created')
        return redirect('task')
    else:
        print(form.errors)
    roots = Task.objects.all().filter(user=user).order_by('-pk')
    paginator = Paginator(roots, 15)
    page = request.GET.get('page', 1)
    result = paginator.get_page(page)
    ctx = {
        "roots": result,
        'p_title': "Task",
        "form": form,
        "status": status
    }
    return render(request, 'pages/task.html', ctx)
