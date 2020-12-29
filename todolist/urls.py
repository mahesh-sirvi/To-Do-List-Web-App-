from django.contrib import admin
from django.urls import path
from tasks import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Home_Page.as_view()),
    path('login', views.Login.as_view()),
    path('register', views.Register.as_view()),
    path('add', views.new_task.as_view()),
    path('all_tasks', views.All_Tasks.as_view()),
    path('delete', views.Delete.as_view()),
    path('today', views.TodayTasks.as_view()),
    path('missed', views.Missed.as_view()),
    path('week', views.Week.as_view()),
]
