import datetime
import uuid
from contextlib import closing

from django.contrib.auth.decorators import login_required
from django.db import connection
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from methodism import generate_key

from base.helper import permission_check
from core.forms.auth import UserForm
from core.models import User


def sign_in(request):
    if request.POST:
        pas = request.POST.get("pass")
        username = request.POST.get("username")
        user = User.objects.filter(username=username).first()
        if not user:
            return render(request, 'auth/login.html', {"error": "Username Yoki Password Xato"})
        if not user.check_password(pas):
            return render(request, 'auth/login.html', {"error": "Username Yoki Password Xato"})
        if not user.is_active:
            return render(request, 'auth/login.html', {"error": "Bu Foydalanuvchi qora ro'yxatda"})

        login(request, user)
        return redirect('home')
    return render(request, 'auth/login.html')


# def sign_up(request):
#     if request.POST:
#         password = request.POST.get("pass")
#         repassword = request.POST.get("re-pass")
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         # user check
#         # user_sql = f"""
#         #     select id from core_user
#         #     where email = '{email}' or username = '{username}'
#         # """
#         # with closing(connection.cursor()) as cursor:
#         #     cursor.execute(user_sql)
#         #     user = cursor.fetchone()
#         #     print(user)
#         user = User.objects.get(username=username)
#         if user:
#             return render(request, 'auth/regis.html', {'error': 'Ushbu username yoki email alaqachon mavjud'})

#         if password != repassword:
#             return render(request, 'auth/regis.html', {'error': 'parol mos kelmadi'})

#         return redirect('login')

from django.shortcuts import render, redirect
from core.models.auth import User


def sign_up(request):
    if request.method == "POST":
        password = request.POST.get("pass")
        repassword = request.POST.get("re-pass")
        username = request.POST.get('username')
        email = request.POST.get('email')

        # Check if user with the same username or email already exists
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            return render(request, 'auth/regis.html', {'error': 'Ushbu username yoki email alaqachon mavjud'})

        if password != repassword:
            return render(request, 'auth/regis.html', {'error': 'Parollar mos kelmadi'})

        # Create and save new user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        return redirect('login')

    return render(request, 'auth/register.html')


@login_required(login_url='login')
def sign_out(request):
    logout(request)
    return redirect('login')


@permission_check
def manage_user(request, ut, pk=None, status='list'):
    user = User.objects.filter(pk=pk).first() or None
    form = UserForm(request.POST or None, request.FILES or None, instance=user)
    if form.is_valid():
        user = form.save()
    else:
        print(form.errors)
    ctx = {
        "form": form,
        "status": status,
        "ut": ut,
        "user": user

    }
    return render(request, 'pages/users.html', ctx)


@permission_check
def change_password(request, user_id):
    user = User.objects.filter(id=user_id).first()
    if request.POST:
        if user == request.user:
            request.user.set_password(request.POST.get('password'))
            request.user.save()
        else:
            user.set_password(request.POST.get('password'))
            user.save()
    return redirect('users', ut=user.user_type)


@permission_check
def user_profile(request, user_id):
    user = User.objects.filter(id=user_id).first()
    if not user:
        return render(request, "base.html", {'error': 404})
    ctx = {
        "user": user
    }
    return render(request, 'pages/user-profile.html', ctx)
