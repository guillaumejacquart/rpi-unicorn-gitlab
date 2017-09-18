from tinydb import Query
from gitlab_projects import project_status
from db_init import db

def setDbFromProjects():
    print 'Init projects db from gitlab ...'
    projects = project_status();
    Conf = Query()
    
    for p, status in projects.iteritems():
        c = db.search(Conf.name == p)
        if len(c) == 0:
            db.insert({'name': p, 'row': 0, 'col': 0, 'status': status, 'active': False, 'type': 'project'})