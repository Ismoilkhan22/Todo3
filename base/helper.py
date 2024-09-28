import random
from contextlib import closing

from django.core.paginator import Paginator
from django.db import connection
from django.shortcuts import redirect, render
from methodism import dictfetchone

from datetime import datetime as dt

from core.models.task import Task


def permission_check(funk):
    def wrapper(request, *args, **kwargs):
        if request.user.is_anonymous:
            return redirect('login')
        if request.user.user_type != 1:
            return render(request, "base.html", {'error': 404})

        return funk(request, *args, **kwargs)

    return wrapper


def counter(id):
    sql = f'''
    select 
    ( select COUNT(*) from core_task WHERE user_id={id} ) as task,
    (select COUNT(*) from core_user us WHERE us.user_type=1) as admin,
    (select COUNT(*) from core_user us WHERE us.user_type=2) as costumer
    from core_user
    limit 1
    '''
    with closing(connection.cursor()) as cursor:
        cursor.execute(sql)
        natija = dictfetchone(cursor)
    return natija


def user_home(request):
    roots = Task.objects.all().order_by('-pk')
    return {
        "task": roots,
    }
