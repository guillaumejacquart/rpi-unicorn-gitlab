from tinydb import TinyDB, Query
db = TinyDB('db.json')

def getGitlabApiKeys():
    gitlab_keys_table = db.table('gitlab_keys')
    return gitlab_keys_table.all()

def setGitlabApiKeys(conf):
    db.purge_table('gitlab_keys')
    gitlab_keys_table = db.table('gitlab_keys')
    gitlab_keys_table.insert({'url': conf['url'], 'secret': conf['secret']})