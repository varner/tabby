from __future__ import unicode_literals
from django.db import models

import json
import urllib2


class RecievedMessage(models.Model):
    body = models.TextFiled(_("Body"))

'''
def get_moon_phase(month, day, year):
    # month: int, 1 - 12
    # day:   int, 1 - 31
    # year:  int, 1700 - 2100

    url = "http://api.usno.navy.mil/moon/phase?date=%d/%d/%d&nump=1" % (month, day, year)
    response = urllib2.urlopen(url)
    data = json.load(response)
    phase = data['phasedata'][0]['phase']

    # there's only four phases! we're just converting them into numbers because whatever
    if   phase == u'New Moon':      return 0
    elif phase == u'First Quarter': return 1
    elif phase == u'Full Moon':     return 2
    elif phase == u'Last Quarter':  return 3

    # if there's a totally different phase then we've really fucked up! return -1 to signal for help
    return -1
'''