import colorsys
import math
import time
from apscheduler.schedulers.background import BackgroundScheduler
from tinydb import Query
import logging
logging.basicConfig()

from manager.gitlab_projects import project_status
from manager.db_init import db

def refresh():
    print 'Init projects refresh ...'
    projects = project_status();
    Conf = Query()
    
    print 'Setting values...'
    for p, status in projects.iteritems():
        c = db.search(Conf.name == p)
        if len(c) > 0:
            if c[0]['active']:
                color = ('green' if status == 'success' else 'red')
                strCon = 'light led {},{} with color {}'.format(c[0]['row'], c[0]['col'], color)
                print strCon
        else:
            db.insert({'name': p, 'row': 0, 'col': 0, 'status': status, 'active': False, 'type': 'project'})
    
    print 'Done refreshing !'
    
def init():
    sched = BackgroundScheduler()
    sched.start() 
    job = sched.add_job(refresh, 'interval', minutes=1)
        