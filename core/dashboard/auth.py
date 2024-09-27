import datetime
import uuid

from django.contrib.auth.decorators import login_required
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

