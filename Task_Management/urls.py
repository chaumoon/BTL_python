from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name='Register'),
    path('login/', views.login, name = 'Login'),
    path('forgot/', views.forgot, name = 'Forgot'),
    path('task/', views.task, name = 'Task'),
    path('today/', views.task, {'task_type': 'today'}, name = 'Today'),
    path('week/', views.task, {'task_type': 'week'}, name = 'Week'),
    path('completed/', views.task, {'task_type': 'completed'}, name = 'Completed'),
    path('overdue/', views.task, {'task_type': 'overdue'}, name = 'Overdue'),
    path('add/', views.task, name='Add_task'),
    path('update-task-status/', views.update_task_status, name='update_task_status'),
    path('delete-task/', views.delete_task, name='DeleteTask'),
    path('edit-task/', views.edit_task, name='EditTask'),
    path('logout/', views.logout, name = 'Logout'),
]