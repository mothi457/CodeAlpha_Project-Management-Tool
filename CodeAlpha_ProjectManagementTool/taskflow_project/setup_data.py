#!/usr/bin/env python
"""
TaskFlow Setup Script — Run this to initialize the project with sample data
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskflow.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth.models import User
from projects.models import Project, TaskBoard, Task, Notification

print("🚀 Setting up TaskFlow...")

# Create users
users = []
for uname, email, pw in [
    ('admin', 'admin@taskflow.com', 'admin123'),
    ('alice', 'alice@taskflow.com', 'alice123'),
    ('bob', 'bob@taskflow.com', 'bob123'),
]:
    if not User.objects.filter(username=uname).exists():
        if uname == 'admin':
            u = User.objects.create_superuser(uname, email, pw)
        else:
            u = User.objects.create_user(uname, email, pw)
        print(f"  ✅ Created user: {uname}")
    else:
        u = User.objects.get(username=uname)
    users.append(u)

admin_user, alice, bob = users

# Create sample projects
projects_data = [
    {
        'name': 'Mobile App Redesign',
        'description': 'Complete UI/UX overhaul of the main mobile application',
        'color': '#6366f1',
        'tasks': [
            ('Design new onboarding flow', 'Create wireframes and mockups for improved user onboarding experience', 'high', 'in_progress', alice),
            ('Implement dark mode', 'Add system-wide dark mode support across all screens', 'medium', 'todo', bob),
            ('Fix navigation bugs', 'Resolve reported issues with bottom navigation bar', 'urgent', 'in_progress', alice),
            ('Write unit tests', 'Achieve 80% code coverage for core modules', 'low', 'todo', None),
            ('App store submission', 'Prepare assets and submit to App Store and Play Store', 'high', 'todo', bob),
            ('Performance optimization', 'Reduce app launch time by 40%', 'medium', 'done', alice),
        ]
    },
    {
        'name': 'E-Commerce Platform',
        'description': 'Build a scalable online marketplace with Django & React',
        'color': '#22c55e',
        'tasks': [
            ('Setup Django REST API', 'Create RESTful endpoints for products, orders, and users', 'high', 'done', admin_user),
            ('Integrate payment gateway', 'Add Razorpay/Stripe payment processing', 'urgent', 'in_progress', alice),
            ('Product search feature', 'Implement Elasticsearch for fast product search', 'medium', 'todo', bob),
            ('Admin dashboard', 'Build analytics dashboard for store owners', 'medium', 'review', alice),
            ('Email notifications', 'Setup transactional emails for orders and shipping', 'low', 'todo', None),
        ]
    },
    {
        'name': 'CodeAlpha Internship Tasks',
        'description': 'Track all internship tasks and deliverables',
        'color': '#f59e0b',
        'tasks': [
            ('Task 1: E-Commerce Store', 'Simple e-commerce site with cart, auth, and orders', 'high', 'done', admin_user),
            ('Task 3: Project Management Tool', 'Collaborative tool like Trello with real-time features', 'high', 'in_progress', admin_user),
            ('Record demo videos', 'Screen record all completed projects for LinkedIn', 'medium', 'todo', admin_user),
            ('Upload to GitHub', 'Push all project code to GitHub repositories', 'high', 'in_progress', admin_user),
            ('LinkedIn posts', 'Write and publish posts about each completed task', 'medium', 'todo', admin_user),
            ('Submit to CodeAlpha', 'Fill submission form with GitHub and LinkedIn links', 'urgent', 'todo', admin_user),
        ]
    },
]

for proj_data in projects_data:
    if Project.objects.filter(name=proj_data['name']).exists():
        print(f"  ⏭ Project already exists: {proj_data['name']}")
        continue

    project = Project.objects.create(
        name=proj_data['name'],
        description=proj_data['description'],
        color=proj_data['color'],
        owner=admin_user,
    )
    project.members.add(alice, bob)

    boards = {}
    for i, board_name in enumerate(['To Do', 'In Progress', 'In Review', 'Done']):
        board = TaskBoard.objects.create(project=project, name=board_name, order=i)
        boards[board_name] = board

    status_to_board = {
        'todo': boards['To Do'],
        'in_progress': boards['In Progress'],
        'review': boards['In Review'],
        'done': boards['Done'],
    }

    for title, desc, priority, status, assigned in proj_data['tasks']:
        Task.objects.create(
            project=project,
            board=status_to_board[status],
            title=title,
            description=desc,
            priority=priority,
            status=status,
            assigned_to=assigned,
            created_by=admin_user,
        )

    print(f"  ✅ Created project: {proj_data['name']} with {len(proj_data['tasks'])} tasks")

# Sample notifications
if not Notification.objects.filter(user=admin_user).exists():
    Notification.objects.create(user=admin_user, message='Welcome to TaskFlow! 🎉 Create your first project.', link='/projects/')
    Notification.objects.create(user=admin_user, message='Alice commented on "Design new onboarding flow"')
    Notification.objects.create(user=alice, message='You were assigned task "Fix navigation bugs"')
    Notification.objects.create(user=bob, message='You were added to project "Mobile App Redesign"')
    print("  ✅ Created sample notifications")

print("\n✅ TaskFlow setup complete!")
print("\n📌 Login credentials:")
print("   Admin : admin / admin123 (http://127.0.0.1:8000/admin)")
print("   Alice : alice / alice123")
print("   Bob   : bob / bob123")
print("\n🌐 Run: python manage.py runserver")
print("   Open: http://127.0.0.1:8000")
