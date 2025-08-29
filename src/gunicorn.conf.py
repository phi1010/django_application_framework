import multiprocessing

from prometheus_client import multiprocess, CollectorRegistry

bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
max_requests = 1000
max_requests_jitter = 100


def post_worker_init(worker):
    pass # TODO initialize worker here if needed, e.g. persistent connections, etc.


def when_ready(_):
    multiprocess.MultiProcessCollector(CollectorRegistry())


def child_exit(_, worker):
    multiprocess.mark_process_dead(worker.pid)