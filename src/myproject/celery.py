import logging
import os
import sys

from celery import Celery, shared_task
from celery.signals import worker_init, worker_ready, worker_process_shutdown, worker_process_init, celeryd_init
from prometheus_client import start_http_server, CollectorRegistry, multiprocess

log = logging.getLogger(__name__)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

app = Celery('myproject')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@celeryd_init.connect()
def worker_init_handler(*args, **kwargs):
    log.info(f"Celeryd Init {args, kwargs!r}")
    try:
        registry = CollectorRegistry()
        multiprocess.MultiProcessCollector(registry)
        # Start Prometheus metrics server
        port = 8001
        start_http_server(port, registry=registry)
        log.info(f"Started prometheus server on port {port}")
    except Exception as e:
        log.error(e)

@worker_ready.connect()
def worker_ready_handler(*args, **kwargs):
    log.info(f"Worker Ready {args, kwargs!r}")

@worker_process_shutdown.connect()
def worker_process_shutdown_handler(*args, **kwargs):
    log.info(f"Worker Process Shutdown {args, kwargs!r}")
    try:
        multiprocess.mark_process_dead(os.getpid())
    except Exception as e:
        log.error(e)