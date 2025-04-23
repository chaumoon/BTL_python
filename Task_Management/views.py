from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Account, Tag, Task

# Create your views here.

def register(request):
    return render(request, 'register.html')

def register(request):
    notice = None
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')
        if Account.objects.filter(username=username).exists():
            if notice == None:
                notice = "Sử dụng tên đăng nhập khác"
            return render(request, 'register.html', {'notice': notice})
        elif Account.objects.filter(email=email).exists():
            if notice == None:
                notice = "Email này đã được sử dụng"
            return render(request, 'register.html', {'notice': notice})
        if password != confirm_password:
            notice = "Mật khẩu không khớp"
            return render(request, 'register.html', {'notice': notice})
        else:
            user = Account(username=username, email=email, password=password)
            user.save()    
            return redirect('Login')
    else:
        return render(request, 'register.html')

def login(request):
    if request.session.get('logged_in'):
        if request.session.get('username') == 'python':
            return redirect('/admin/')
        else:
            return redirect('User')
    notice = None
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = Account.objects.get(username=username)
            if password == user.password:
                request.session['user_id'] = user.id
                request.session['username'] = user.username
                request.session['logged_in'] = True
                if user.username == 'python':
                    return redirect('/admin/')
                else:
                    return redirect('User')
            else:
                if notice == None:
                    notice = "Sai tên đăng nhập hoặc mật khẩu!"
        except Account.DoesNotExist:
            if notice == None:
                notice = "Sai tên đăng nhập hoặc mật khẩu!"
        return render(request, 'login.html', {'notice': notice})
    else:
        return render(request, 'login.html')

def forgot(request):
    if request.method == "POST":
        notice = None
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = Account.objects.get(username=username)
            if email != user.email:
                if notice == None:
                    notice = "Tên đăng nhập hoặc email không đúng"
                    return render(request, 'forgot.html', {'notice': notice})
            else:
                message = f"Mật khẩu của bạn là: {user.password}"
                return render(request, 'forgot.html', {'message': message})
        except Account.DoesNotExist:
            if notice == None:
                notice = "Tên đăng nhập hoặc email không đúng"
            return render(request, 'forgot.html', {'notice': notice})
    else:
        return render(request, 'forgot.html')

