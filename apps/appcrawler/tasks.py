# -*-coding:utf-8-*-
# 请求的异步任务调度

from MAT.celery import app
import startappium

@app.task
def build_job(job):
    return startappium.Foo(job)





