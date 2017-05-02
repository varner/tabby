from __future__ import absolute_import, unicode_literals
from celery import shared_task

schedule = {"daily":
    [{ "start": datetime.time(7, 30, 0),
      "end": datetime.time(10, 30, 0)
    }, 
    { "start": datetime.time(13, 0, 0),
      "end": datetime.time(17, 20, 0)
    },
    { "start": datetime.time(19, 11, 0),
      "end": datetime.time(19, 55, 0)
    },
    { "start": datetime.time(20, 5, 0),
      "end": datetime.time(23, 3, 20)
    }]
}

@shared_task
def process_message(id):
    return x + y