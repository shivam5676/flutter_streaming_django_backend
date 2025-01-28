from celery import Celery

app = Celery("your_project")

# Use Redis as broker
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks from installed apps
app.autodiscover_tasks()
