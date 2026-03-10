from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # Projects
    path('projects/', views.project_list, name='project_list'),
    path('projects/create/', views.project_create, name='project_create'),
    path('project/<int:pk>/', views.project_detail, name='project_detail'),
    path('project/<int:pk>/add-member/', views.add_member, name='add_member'),
    path('project/<int:pk>/remove-member/', views.remove_member, name='remove_member'),

    # Tasks
    path('project/<int:project_pk>/task/create/', views.task_create, name='task_create'),
    path('task/<int:pk>/', views.task_detail, name='task_detail'),
    path('task/<int:pk>/status/', views.task_update_status, name='task_update_status'),
    path('task/<int:pk>/delete/', views.task_delete, name='task_delete'),

    # Comments
    path('task/<int:task_pk>/comment/', views.add_comment, name='add_comment'),

    # Attachments
    path('task/<int:task_pk>/attach/', views.upload_attachment, name='upload_attachment'),
    path('attachment/<int:pk>/delete/', views.delete_attachment, name='delete_attachment'),

    # Notifications
    path('notifications/', views.notifications_list, name='notifications'),
    path('notifications/read/', views.mark_notifications_read, name='mark_read'),
]
