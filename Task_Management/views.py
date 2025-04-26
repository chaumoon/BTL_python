from django.http import HttpResponse, request
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Account, Tag, Task
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware, is_naive
from datetime import timedelta, datetime


# Create your views here.

def register(request):
    request.session['user_id'] = False
    error = None
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')
        if Account.objects.filter(username=username).exists() or username=='admin':
            if error == None:
                error = "Sử dụng tên đăng nhập khác"
            return render(request, 'register.html', {'error': error})
        elif Account.objects.filter(email=email).exists():
            if error == None:
                error = "Email này đã được sử dụng"
            return render(request, 'register.html', {'error': error})
        if password != confirm_password:
            error = "Mật khẩu không khớp"
            return render(request, 'register.html', {'error': error})
        else:
            user = Account(username=username, email=email, password=password)
            user.save()    
            return redirect('Login')
    else:
        return render(request, 'register.html')

def login(request):
    if request.session.get('user_id') and request.session.get('username') != 'admin':
        return redirect('Task')
    error = None
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = Account.objects.get(username=username)
            if password == user.password:
                request.session['user_id'] = user.id
                request.session['username'] = user.username
                request.session['logged_in'] = True
                if user.username != 'admin':
                    return redirect('Task')
                else:
                    if error == None:
                        error = "Sai tên đăng nhập hoặc mật khẩu!"
                    return render(request, 'login.html', {'error': error})
            else:
                if error == None:
                    error = "Sai tên đăng nhập hoặc mật khẩu!"
                return render(request, 'login.html', {'error': error})
        except Account.DoesNotExist:
            if error == None:
                error = "Sai tên đăng nhập hoặc mật khẩu!"
            return render(request, 'login.html', {'error': error})
    else:
        return render(request, 'login.html')

def forgot(request):
    request.session['user_id'] = False
    if request.method == "POST":
        error = None
        username = request.POST.get('username')
        email = request.POST.get('email')
        try:
            user = Account.objects.get(username=username)
            if email != user.email or username == 'admin':
                if error == None:
                    error = "Tên đăng nhập hoặc email không đúng"
                    return render(request, 'forgot.html', {'error': error})
            else:
                message = f"Mật khẩu của bạn là: {user.password}"
                return render(request, 'forgot.html', {'message': message})
        except Account.DoesNotExist:
            if error == None:
                error = "Tên đăng nhập hoặc email không đúng"
            return render(request, 'forgot.html', {'error': error})
    else:
        return render(request, 'forgot.html')

def task(request, task_type=None):
    if request.method != "POST":
        if 'user_id' not in request.session:
            return redirect('Login')
        try:
            account = Account.objects.get(id=request.session['user_id'])
            tasks = Task.objects.filter(account=account) 
            tags = Tag.objects.all() 

            now = timezone.now()
            today = now.date()
            if task_type == 'today':
                tasks = tasks.filter(
                    dl__date=today,
                    dl__gte=now,
                    is_completed=False
                ).order_by('dl')
                
            elif task_type == 'week':
                end_week = today + timedelta(days=7)
                tasks = tasks.filter(
                    dl__range=[now, end_week], 
                    is_completed=False
                ).order_by('dl')
                
            elif task_type == 'completed':
                tasks = tasks.filter(
                    is_completed=True
                ).order_by('dl') 
                
            elif task_type == 'overdue':
                tasks = tasks.filter(
                    dl__lt=now,
                    is_completed=False
                ).order_by('dl')  
                
            else:
                tasks = tasks.filter(
                    dl__gte=now,
                    is_completed=False
                ).order_by('dl')
            return render(request, 'task.html', {
                'tasks': tasks,
                'tags': tags,
            })
        except Account.DoesNotExist:
            return redirect('Login')
    else:
        if 'user_id' not in request.session:
            return redirect('Login')
        try:
            account = Account.objects.get(id=request.session['user_id'])
            name = request.POST.get('name')
            dl_str = request.POST.get('dl')
            dl = parse_datetime(dl_str)

            if dl is not None:
                if timezone.is_naive(dl):
                    dl = make_aware(dl)
                if dl < timezone.now():
                    dl = None
            else:
                dl = None
            tag_id = request.POST.get('tag')
            des = request.POST.get('des', '')

            if not (name and dl and tag_id):
                tasks = Task.objects.filter(account=account)
                tags = Tag.objects.all()
                return render(request, 'task.html', {
                    'tasks': tasks,
                    'tags': tags,
                    'error': 'Thiếu thông tin'
                })

            try:
                tag = Tag.objects.get(id=tag_id)
            except Tag.DoesNotExist:
                tasks = Task.objects.filter(account=account)
                tags = Tag.objects.all()
                return render(request, 'task.html', {
                    'tasks': tasks,
                    'tags': tags,
                    'error': 'Tag không tồn tại'
                })

            Task.objects.create(
                name=name,
                dl=dl,
                des=des,
                tag=tag,
                account=account
            )
            tasks = Task.objects.filter(account=account)
            tags = Tag.objects.all()

            now = timezone.now()
            today = now.date()
            if task_type == 'today':
                tasks = tasks.filter(
                    dl__date=today,
                    dl__gte=now,
                    is_completed=False
                ).order_by('dl')
                
            elif task_type == 'week':
                end_week = today + timedelta(days=7)
                tasks = tasks.filter(
                    dl__range=[now, end_week], 
                    is_completed=False
                ).order_by('dl')
                
            elif task_type == 'completed':
                tasks = tasks.filter(
                    is_completed=True
                ).order_by('dl') 
                
            elif task_type == 'overdue':
                tasks = tasks.filter(
                    dl__lt=now,
                    is_completed=False
                ).order_by('dl')  
                
            else:
                tasks = tasks.filter(
                    dl__gte=now,
                    is_completed=False
                ).order_by('dl')
            return render(request, 'task.html', {
                'tasks': tasks,
                'tags': tags,
                'message': 'Thêm công việc thành công!'  
            })

        except Account.DoesNotExist:
            return redirect('Login')

def update_task_status(request):
    if request.method == "POST":
        task_id = request.POST.get('id')
        is_completed = request.POST.get('is_completed').lower() == 'true'

        try:
            task = Task.objects.get(id=task_id)
            task.is_completed = is_completed
            task.save()
            return HttpResponse("OK")
        except Exception as e:
            return HttpResponse("ERROR", status=400) 
    return HttpResponse("Invalid method", status=405)

from django.shortcuts import get_object_or_404


def delete_task(request):
    if 'user_id' not in request.session:
        return redirect('Login') 

    if request.method == 'POST':
        task_id = request.POST.get('id')
        task = get_object_or_404(Task, id=task_id, account_id=request.session['user_id'])
        task.delete()
    return redirect(request.META.get('HTTP_REFERER', 'Task'))

def edit_task(request):
    if request.method != 'POST':
        return redirect(request.META.get('HTTP_REFERER', 'Task'))
    
    try:
        task_id = request.POST.get('id')
        task = get_object_or_404(Task, id=task_id)
        
        name = request.POST.get('name', '').strip()
        dl = request.POST.get('dl')
        tag_id = request.POST.get('tag')
        des = request.POST.get('des', '').strip()
        
        if not name:
            return redirect(request.META.get('HTTP_REFERER', 'Task'))
            
        if not dl:
            return redirect(request.META.get('HTTP_REFERER', 'Task'))
            
        if not tag_id:
            return redirect(request.META.get('HTTP_REFERER', 'Task'))
            
        task.name = name
        task.dl = dl
        task.tag_id = tag_id
        task.des = des
        task.save()
    
        return redirect(request.META.get('HTTP_REFERER', 'Task'))
        
    except Exception as e:
        return redirect(request.META.get('HTTP_REFERER', 'Task'))

def logout(request):
    if request.method == "POST":
        request.session.flush() 
        return redirect('Register') 