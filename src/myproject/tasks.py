import random
import time

from .celery import app
import logging
from prometheus_client import start_http_server, Counter, Histogram

log = logging.getLogger(__name__)
task_counter = Counter('celery_debug_task_total', 'Total number of Celery debug_tasks called')
task_duration = Histogram('celery_debug_task_duration', 'Histogram of Celery debug_tasks duration')


@app.task(bind=True)
@task_duration.time()
def debug_task(self):
    task_counter.inc()
    log.info(f'Request: {self.request!r}')
    time.sleep(random.randint(0,30))  # Simulate a long-running task
