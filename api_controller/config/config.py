import os

from prometheus_client import multiprocess


def get_workers():
    try:
        worker = os.environ["GUNICORN_WORKERS"]
    except KeyError:
        worker = 2
    return worker


def get_threads():
    try:
        thread = os.environ["GUNICORN_THREADS"]
    except KeyError:
        thread = 2
    return thread


def get_worker_class():
    try:
        worker_c = os.environ["GUNICORN_WORKER_CLASS"]
    except KeyError:
        worker_c = 'gthreads'
    return worker_c


def get_worker_connections():
    try:
        connections = os.environ["GUNICORN_WORKER_CONNECTIONS"]
    except KeyError:
        connections = 1000
    return connections


def get_keepalive():
    try:
        keepalive_ = os.environ["GUNICORN_KEEPALIVE"]
    except KeyError:
        keepalive_ = 60
    return keepalive_


def get_timeout():
    try:
        timeout_ = os.environ["GUNICORN_TIMEOUT"]
    except KeyError:
        timeout_ = 60
    return timeout_


bind = "0.0.0.0:9000"
workers = get_workers()
timeout = get_timeout()
keepalive = get_keepalive()
worker_class = get_worker_class()
threads = get_threads()
worker_connections = get_worker_connections()
max_requests = 500

loglevel = 'debug'
capture_output = True
worker_tmp_dir = '/dev/shm'


def worker_exit(server, worker):
    multiprocess.mark_process_dead(worker.pid)


def child_exit(server, worker):
    multiprocess.mark_process_dead(worker.pid)


def when_ready(server):
    server.log.info('Server is ready. Spawning workers..')
