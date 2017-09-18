from flask import Flask, request, jsonify
from tinydb import Query
import os
import manager.gitlab_projects as gitlab_projects
from manager.db_init import db, getGitlabApiKeys, setGitlabApiKeys
from manager.gitlab_db import setDbFromProjects
import refresh

app = Flask(__name__)


@app.route("/", methods=['GET'])
def index():
    return app.send_static_file('index.html')

@app.route("/config", methods=['GET'])
def config():
    Conf = Query()
    results = db.search(Conf.type == 'project');
    return jsonify(results)

@app.route("/config", methods=['POST'])
def config_save():
    Conf = Query()
    
    for c in request.json:
        db.update({'row': c['row'], 'col': c['col'], 'active': c['active']}, Conf.name == c['name'])
    
    return "ok"

@app.route("/keys", methods=['GET'])
def gitlab_keys():
    results = getGitlabApiKeys()
    return jsonify(results)

@app.route("/keys", methods=['PUT'])
def gitlab_keys_save():
    setGitlabApiKeys(request.json)
    gitlab_projects.init(request.json)
    setDbFromProjects()
    
    return "ok"
    
@app.before_first_request
def initialize():
    gitlab_keys = getGitlabApiKeys()
    
    if len(gitlab_keys) > 0:
        print 'Init Gitlab connection and authentication'
        gitlab_projects.init(gitlab_keys[0])
    
    print 'Init scheduler to refresh project status'
    refresh.init()
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ['PORT'] or 8080), debug=True)