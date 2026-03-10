from django.contrib import admin
from .models import Project, Task, TaskBoard, Comment, Attachment, Notification

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'created_at']

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'project', 'status', 'priority', 'assigned_to', 'due_date']
    list_filter = ['status', 'priority']
    list_editable = ['status', 'priority']

@admin.register(TaskBoard)
class TaskBoardAdmin(admin.ModelAdmin):
    list_display = ['name', 'project', 'order']

admin.site.register(Comment)
admin.site.register(Attachment)
admin.site.register(Notification)
