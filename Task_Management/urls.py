from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name='Register'),
    path('login/', views.login, name = 'Login'),
    path('forgot/', views.forgot, name = 'Forgot'),
    path('task/', views.task, name = 'Task'),
    # path('logout/', views.logout, name = 'Logout'),
]