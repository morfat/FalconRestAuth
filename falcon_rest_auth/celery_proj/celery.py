from __future__ import absolute_import,unicode_literals
from celery import Celery

app = Celery('falcon_rest_auth',
              broker = 'pyamqp://guest@localhost//',
              include = ['falcon_rest_auth.celery_proj.tasks'] 
            )


if __name__ == '__main__':
    app.start()
