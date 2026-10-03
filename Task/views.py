# --------------------------
# views.py
# --------------------------
from django.shortcuts import render, redirect
from .models import User, Task, Team
from django.contrib.auth.hashers import make_password, check_password
import secrets

# Register view with team selection
def register_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        password = request.POST.get('password')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        team_id = request.POST.get('team_id')

        team = Team.objects.filter(id=team_id).first()
        if not team:
            return render(request, 'components/register.html', {'error': 'Invalid Team ID', 'teams': Team.objects.all()})

        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            return render(request, 'components/register.html', {'error': 'Username or Email already exists', 'teams': Team.objects.all()})

        hashed_password = make_password(password)
        user = User.objects.create(
            username=username,
            firstname=firstname,
            lastname=lastname,
            password=hashed_password,
            email=email,
            phone=phone,
            team=team
        )
        user.save()
        request.session['user_id'] = user.id
        return redirect('choose_role')
    teams = Team.objects.all()
    return render(request, 'components/register.html', {'teams': teams})

# Login view
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username=username).first()
        if user and check_password(password, user.password):
            token = secrets.token_hex(16)
            request.session['user_id'] = user.id
            return redirect('home')
        return render(request, 'components/login.html', {'error': 'Login failed'})
    return render(request, 'components/login.html')

# Choose Role view
def choose_role_view(request):
    if request.method == "POST":
        role = request.POST.get('role')
        user_id = request.session.get('user_id')
        user = User.objects.filter(id=user_id).first()
        if user:
            user.role = role
            user.save()
            return redirect('login')
    return render(request, 'components/choose_role.html')

# Home view with filter by status OR responsible
def home_view(request):
    user_id = request.session.get('user_id')
    user = User.objects.filter(id=user_id).first() if user_id else None
    tasks = Task.objects.all()

    status_filter = request.GET.get('status')
    responsible_filter = request.GET.get('responsible')

    if status_filter:
        tasks = tasks.filter(status=status_filter)
    elif responsible_filter:
        tasks = tasks.filter(responsible__id=responsible_filter)

    return render(request, 'components/home.html', {
        'user': user,
        'tasks': tasks,
        'users': User.objects.all()
    })

# Associate task
def associate_task_view(request, task_id):
    user_id = request.session.get('user_id')
    user = User.objects.filter(id=user_id).first()
    task = Task.objects.filter(id=task_id).first()
    if user and task and user.role == User.Role.EMPLOYEE and task.responsible is None:
        task.responsible = user
        task.status = Task.Status.IN_PROCESS
        task.save()
    return redirect('home')

# Report completed
def report_completed_view(request, task_id):
    user_id = request.session.get('user_id')
    user = User.objects.filter(id=user_id).first()
    task = Task.objects.filter(id=task_id).first()
    if user and task and task.responsible == user:
        task.status = Task.Status.COMPLETED
        task.save()
    return redirect('home')

# Add task
def add_task_view(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        Task.objects.create(title=title, description=description)
        return redirect('home')
    return render(request, 'add_task.html')

# Update task
def update_task_view(request, task_id):
    task = Task.objects.filter(id=task_id).first()
    if request.method == "POST":
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.status = request.POST.get('status')
        task.save()
        return redirect('home')
    return render(request, 'update_task.html', {'task': task})

# Delete task
def delete_task_view(request, task_id):
    task = Task.objects.filter(id=task_id, responsible__isnull=True).first()
    if task:
        task.delete()
    return redirect('home')

# Logout view
def logout_view(request):
    request.session.flush()
    return redirect('login')
