# --------------------------
# urls.py
# --------------------------
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('associate/<int:task_id>', views.associate_task_view, name='associate_task'),
    path('report_completed/<int:task_id>', views.report_completed_view, name='report_completed'),
    path('add_task', views.add_task_view, name='add_task'),
    path('update_task/<int:task_id>', views.update_task_view, name='update_task'),
    path('delete_task/<int:task_id>', views.delete_task_view, name='delete_task'),
    path('register', views.register_view, name='register'),
    path('login', views.login_view, name='login'),
    path('choose_role', views.choose_role_view, name='choose_role'),
    path('logout', views.logout_view, name='logout'),
]
