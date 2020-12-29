from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from tasks.models import New_Task
from django.contrib.auth import authenticate, login, logout
import datetime
from datetime import timedelta
from django.contrib import messages

class Home_Page(View):
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            if request.user.is_authenticated:
                messages.warning(request, 'Logged out successfully from {}'.format(request.user))
                logout(request)
                return redirect('/')

    def get(self, requst, *args, **kwargs):
        return render(requst, 'home_page.html')


class Login(View):
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            print(username)
            print(password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Successfully logged in as {}'.format(username))
                return redirect('/')
            else:
                messages.warning(request, 'Incorrect values entered. Please try again.')
                return redirect('/login')

    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')


class Register(View):
    form = UserCreationForm()
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'User created succesfully!')
                return redirect('/')
            else:
                messages.warning(request, 'Incorrect values entered. Please try again.')
                return redirect('/register')
    def get(self, request, *args, **kwargs):
        context = {'form':self.form}
        return render(request, 'register.html', context=context)


class new_task(View):
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            task_description = request.POST.get('description')
            deadline = request.POST.get('deadline')

            today = datetime.datetime.today().date()
            format = "%Y-%m-%d"
            dead = datetime.datetime.strptime(deadline, format)
            dead_line = dead.date()
            days = dead_line - today
            str_days = days.days
            if str_days < 0:
                remark = 'Deadline reached'
            else:
                remark = 'You have {} days left to finish this task'.format(str_days)
            if len(task_description) != 0:
                add_task = New_Task(task=task_description, dead_line=deadline, user=request.user, days=remark)
                add_task.save()
                messages.success(request, 'Task added sucessfully!')
                return redirect('/')
            else:
                return redirect('/add')
    def get(self, request, *args, **kwargs):
        return render(request, 'add.html')

class All_Tasks(View):
    def get(self, request, *args, **kwargs):
        all_tasks = New_Task.objects.all().filter(user=request.user)
        print(len(all_tasks))
        a = New_Task.objects.values_list('dead_line')
        today = datetime.datetime.today().date()
        days_list = []
        for x in a:
            days_list.append((x[0] - today).days)
        empty = []
        for x in days_list:
            if x < 0:
                empty.append('Deadline reached')
            else:
                empty.append(x)

        context = {'task':all_tasks, 'days':empty}
        return render(request, 'all_tasks.html', context=context)


class Delete(View):
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            all_tasks = New_Task.objects.all().filter(user=request.user)
            b = request.POST
            empty = []
            for x in b:
                empty.append(x)
            empty.pop(0)
            empty.pop(-1)
            for x in empty:
                New_Task.objects.filter(user=request.user, task=x).delete()
            if len(request.POST) > 2:
                messages.warning(request, 'Tasks deleted sucessfully!')
                return redirect('/')
            else:
                return redirect('/delete')

    def get(self, request, *args, **kwargs):
        all_tasks = New_Task.objects.all().filter(user=request.user)
        context = {'task': all_tasks}
        return render(request, 'delete.html', context=context)

class TodayTasks(View):
    def get(self, request, *args, **kwargs):
        today = datetime.datetime.today().date()
        todays_tasks = New_Task.objects.filter(dead_line=today)
        for x in todays_tasks:
            print(x)
        context = {'task':todays_tasks}

        return render(request, 'Today.html', context=context)

class Missed(View):
    def get(self, request, *args, **kwargs):
        missed_tasks = New_Task.objects.filter(user=request.user, days='Deadline reached')
        context = {'task':missed_tasks}
        return render(request, 'missed.html', context=context)


class Week(View):
    def get(self, request, *args, **kwargs):
        today = datetime.datetime.today().date()
        today_srt = str(today)
        print(type(today_srt))
        week = today + timedelta(6)
        week_str = str(week)
        print(type(week_str))
        week_tasks = New_Task.objects.filter(user=request.user, dead_line__range=[today, week])
        context = {'task':week_tasks}
        return render(request, 'week.html', context=context)
