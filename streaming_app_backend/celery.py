import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab
import platform
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'streaming_app_backend.settings')

app = Celery('streaming_app_backend')

# Redis as the broker, MongoDB for storing results
app.conf.broker_url = 'redis://localhost:6379/0'
app.conf.result_backend = f"{settings.MONGODB_URI}/celery_results"
# app.autodiscover_tasks('streaming_app_backend')


app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.beat_schedule = {
    "run_daily_auto_check": {
        "task": "helper_function.autoCheckInPointAllotement.autoCheckInPointAllotement",
        "schedule": crontab(minute=0, hour=0),
    },
}


# Choose correct pool automatically
CELERY_WORKER_POOL = "solo" if platform.system() == "Windows" else "prefork"
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
