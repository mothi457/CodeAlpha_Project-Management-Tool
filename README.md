# ⚡ TaskFlow — Project Management Tool

> A real-time collaborative project management web application built with Django (Python) as part of the **CodeAlpha Full Stack Development Internship**.

---

## 🚀 Live Demo

Run locally at: http://127.0.0.1:8000

---

## 📌 Features

- 🏠 **Dashboard** — Stats overview, assigned tasks, recent notifications
- 📁 **Project Management** — Create projects with color labels & descriptions
- 📋 **Kanban Board** — To Do / In Progress / In Review / Done columns
- ➕ **Task Creation** — Priority levels, due dates, assign to team members
- 💬 **Comments** — AJAX-powered comments on every task (no page reload)
- 📎 **File Attachments** — Upload & download files inside tasks
- ⚡ **WebSocket Live Updates** — Real-time task changes across all users
- 🔔 **Real-time Notifications** — Instant alerts for task assignments & comments
- 👥 **Team Members** — Add/remove members per project
- 🌙 **Dark / Light Mode** — Toggle with one click, saved in browser
- 🛠️ **Admin Panel** — Manage all projects, tasks, and users easily
- 📊 **Sample Data** — 3 projects & 17 tasks pre-loaded

---

## 🧰 Tech Stack

|   Layer     |             Technology            |
| ----------- | --------------------------------- |
| Frontend    | HTML, CSS, JavaScript (Vanilla)   |
| Backend     | Django 5.2 (Python)               |
| Real-time   | Django Channels (WebSockets)      |
| Database    | SQLite3                           |
| Auth        | Django Built-in Auth              |
| Fonts       | Plus Jakarta Sans, JetBrains Mono |

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/mothi457/CodeAlpha_ProjectManagementTool.git
cd CodeAlpha_ProjectManagementTool/taskflow_project
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Migrations
```bash
python manage.py makemigrations projects
python manage.py migrate
```

### 4. Load Sample Data
```bash
python setup_data.py
```

### 5. Start Server
```bash
python manage.py runserver
```

### 6. Open in Browser
```bash
http://127.0.0.1:8000
```

---

## 🔐 Login Credentials

|  Username  |  Password  |    Role    |
| ---------- | ---------- | ---------- |
|  `admin`   | `admin123` |  Superuser |
|  `alice`   | `alice123` |   Member   |
|   `bob`    |  `bob123`  |   Member   |

---

## 🛠️ Admin Panel
```bash
URL      : http://127.0.0.1:8000/admin
Username : admin
Password : admin123
```
---

## 📁 Project Structure

```
taskflow_project/
├── taskflow/                   # Django settings & config
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py                 # WebSocket config
│   └── wsgi.py
├── projects/                   # Main app
│   ├── models.py               # Project, Task, Comment, Attachment, Notification
│   ├── views.py                # All page & AJAX views
│   ├── urls.py                 # URL routes
│   ├── admin.py                # Admin config
│   ├── consumers.py            # WebSocket consumers
│   └── routing.py              # WebSocket URL routing
├── templates/
│   └── projects/               # All HTML templates
│       ├── base.html           # Sidebar, topbar, dark mode
│       ├── dashboard.html      # Stats, tasks, notifications
│       ├── project_detail.html # Kanban board
│       ├── project_list.html   # All projects grid
│       ├── project_form.html   # Create project
│       ├── task_detail.html    # Task view, comments, attachments
│       ├── notifications.html
│       ├── login.html
│       └── register.html
├── static/                     # Static files
├── media/                      # Uploaded attachments
├── setup_data.py               # Sample data script
├── manage.py
└── requirements.txt
```

---

## 🌐 WebSocket Endpoints

|                 Endpoint                |          Purpose          |
| --------------------------------------- | ------------------------- |
| `ws://localhost:8000/ws/notifications/` | Real-time notifications   |
| `ws://localhost:8000/ws/project/<id>/`  | Live project task updates |

---

## 📸 Pages Overview

|    Page      |         URL         |
| ------------ | ------------------- |
|Dashboard     | `/dashboard/`       |
|All Projects  | `/projects/`        |
|Create Project| `/projects/create/` |
|Project Board | `/project/<id>/`    |
|Task Detail   | `/task/<id>/`       |
|Notifications | `/notifications/`   |
|Admin Panel   | `/admin/`           |

---

## 👨‍💻 Author

**Mothilal**

- 🔗 LinkedIn : [www.linkedin.com/in/mothilal-b-659788326](https://www.linkedin.com/in/mothilal-b-659788326)
- 🐙 GitHub   : [https://github.com/mothi457](https://github.com/mothi457)
- 📧 Email    : lalbrothers2430@gmail.com

---

## 🏢 Internship Details

This project was built as **Task 3 — Project Management Tool** of the **CodeAlpha Full Stack Development Internship**.

- 🌐 Website  : [www.codealpha.tech](https://www.codealpha.tech)
- 📧 Email    : services@codealpha.tech

---

## 📄 License

This project is developed for educational purposes as part of the CodeAlpha Internship Program.

---

⭐ **If you found this helpful, please star the repository!**
