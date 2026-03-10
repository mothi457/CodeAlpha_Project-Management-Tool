from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json

from .models import Project, Task, TaskBoard, Comment, Attachment, Notification


def create_notification(user, message, link=''):
    notif = Notification.objects.create(user=user, message=message, link=link)
    channel_layer = get_channel_layer()
    try:
        async_to_sync(channel_layer.group_send)(
            f'notifications_{user.id}',
            {'type': 'notification_message', 'message': message, 'link': link}
        )
    except Exception:
        pass
    return notif


def broadcast_task_update(project_id, action, task_id=None, data=None):
    channel_layer = get_channel_layer()
    try:
        async_to_sync(channel_layer.group_send)(
            f'project_{project_id}',
            {'type': 'task_update', 'action': action, 'task_id': task_id, 'data': data or {}}
        )
    except Exception:
        pass


# ─── Auth ─────────────────────────────────────────────────────────────────────

def landing(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'projects/landing.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Invalid credentials.')
    return render(request, 'projects/login.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return redirect('dashboard')
    return render(request, 'projects/register.html')


def logout_view(request):
    logout(request)
    return redirect('landing')


# ─── Dashboard ────────────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    my_projects = Project.objects.filter(owner=request.user) | Project.objects.filter(members=request.user)
    my_projects = my_projects.distinct().order_by('-updated_at')
    my_tasks = Task.objects.filter(assigned_to=request.user).exclude(status='done').order_by('due_date')[:5]
    notifications = Notification.objects.filter(user=request.user, is_read=False)[:5]
    return render(request, 'projects/dashboard.html', {
        'projects': my_projects,
        'my_tasks': my_tasks,
        'notifications': notifications,
    })


# ─── Projects ─────────────────────────────────────────────────────────────────

@login_required
def project_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        color = request.POST.get('color', '#6366f1')
        project = Project.objects.create(name=name, description=description, owner=request.user, color=color)
        # Create default boards
        for i, board_name in enumerate(['To Do', 'In Progress', 'In Review', 'Done']):
            TaskBoard.objects.create(project=project, name=board_name, order=i)
        messages.success(request, f'Project "{name}" created!')
        return redirect('project_detail', pk=project.pk)
    return render(request, 'projects/project_form.html')


@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if project.owner != request.user and request.user not in project.members.all():
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    boards = project.boards.prefetch_related('tasks__assigned_to', 'tasks__comments').all()
    members = list(project.members.all()) + [project.owner]
    all_users = User.objects.exclude(id__in=[m.id for m in members])
    return render(request, 'projects/project_detail.html', {
        'project': project,
        'boards': boards,
        'members': members,
        'all_users': all_users,
    })


@login_required
def project_list(request):
    projects = (Project.objects.filter(owner=request.user) | Project.objects.filter(members=request.user)).distinct()
    return render(request, 'projects/project_list.html', {'projects': projects})


@login_required
@require_POST
def add_member(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    user_id = request.POST.get('user_id')
    user = get_object_or_404(User, id=user_id)
    project.members.add(user)
    create_notification(user, f'You were added to project "{project.name}"', f'/project/{project.pk}/')
    return JsonResponse({'success': True, 'username': user.username})


@login_required
@require_POST
def remove_member(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    user_id = request.POST.get('user_id')
    user = get_object_or_404(User, id=user_id)
    project.members.remove(user)
    return JsonResponse({'success': True})


# ─── Tasks ────────────────────────────────────────────────────────────────────

@login_required
@require_POST
def task_create(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk)
    data = json.loads(request.body)
    board_id = data.get('board_id')
    board = TaskBoard.objects.filter(id=board_id).first()
    assigned_id = data.get('assigned_to')
    assigned = User.objects.filter(id=assigned_id).first() if assigned_id else None

    task = Task.objects.create(
        project=project,
        board=board,
        title=data.get('title'),
        description=data.get('description', ''),
        priority=data.get('priority', 'medium'),
        status=board.name.lower().replace(' ', '_') if board else 'todo',
        assigned_to=assigned,
        created_by=request.user,
        due_date=data.get('due_date') or None,
    )

    if assigned and assigned != request.user:
        create_notification(assigned, f'You were assigned task "{task.title}" in {project.name}', f'/project/{project.pk}/')

    broadcast_task_update(project.pk, 'created', task.pk, {
        'title': task.title,
        'priority': task.priority,
        'board_id': board_id,
    })

    return JsonResponse({
        'success': True,
        'task': {
            'id': task.pk,
            'title': task.title,
            'priority': task.priority,
            'status': task.status,
            'assigned_to': assigned.username if assigned else None,
            'due_date': str(task.due_date) if task.due_date else None,
            'comment_count': 0,
        }
    })


@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    members = list(task.project.members.all()) + [task.project.owner]
    return render(request, 'projects/task_detail.html', {
        'task': task,
        'comments': task.comments.all(),
        'attachments': task.attachments.all(),
        'members': members,
        'project': task.project,
    })


@login_required
@require_POST
def task_update_status(request, pk):
    task = get_object_or_404(Task, pk=pk)
    data = json.loads(request.body)
    new_status = data.get('status')
    board_id = data.get('board_id')
    task.status = new_status
    if board_id:
        task.board_id = board_id
    task.save()
    broadcast_task_update(task.project.pk, 'status_changed', task.pk, {'status': new_status})
    return JsonResponse({'success': True})


@login_required
@require_POST
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    project_pk = task.project.pk
    task.delete()
    broadcast_task_update(project_pk, 'deleted', pk)
    return JsonResponse({'success': True})


# ─── Comments ─────────────────────────────────────────────────────────────────

@login_required
@require_POST
def add_comment(request, task_pk):
    task = get_object_or_404(Task, pk=task_pk)
    data = json.loads(request.body)
    comment = Comment.objects.create(task=task, author=request.user, content=data.get('content'))

    # Notify task assignee
    if task.assigned_to and task.assigned_to != request.user:
        create_notification(task.assigned_to, f'{request.user.username} commented on "{task.title}"', f'/task/{task.pk}/')

    return JsonResponse({
        'success': True,
        'comment': {
            'id': comment.pk,
            'author': request.user.username,
            'content': comment.content,
            'created_at': comment.created_at.strftime('%d %b %Y, %I:%M %p'),
        }
    })


# ─── Attachments ──────────────────────────────────────────────────────────────

@login_required
@require_POST
def upload_attachment(request, task_pk):
    task = get_object_or_404(Task, pk=task_pk)
    file = request.FILES.get('file')
    if file:
        att = Attachment.objects.create(task=task, uploaded_by=request.user, file=file, filename=file.name)
        return JsonResponse({'success': True, 'filename': att.filename, 'url': att.file.url, 'id': att.pk})
    return JsonResponse({'success': False})


@login_required
def delete_attachment(request, pk):
    att = get_object_or_404(Attachment, pk=pk)
    att.file.delete()
    att.delete()
    return JsonResponse({'success': True})


# ─── Notifications ────────────────────────────────────────────────────────────

@login_required
def notifications_list(request):
    notifs = Notification.objects.filter(user=request.user).order_by('-created_at')[:30]
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return render(request, 'projects/notifications.html', {'notifications': notifs})


@login_required
def mark_notifications_read(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return JsonResponse({'success': True})
