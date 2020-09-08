from celery import Celery
import sys

sys.path.append("/home/ztf/IdeaProjects/Demo/celeryDemo/example/")
app = Celery()
app.config_from_object('celeryconfig')


@app.task
def add(x, y):
    return x + y
