import gitlab

gl = None

def init(conf):
    global gl
    # private token authentication
    gl = gitlab.Gitlab(conf['url'], conf['secret'])
    
    # make an API request to create the gl.user object. This is mandatory if you
    # use the username/password authentication.
    gl.auth()
    
    return gl

#import unicornhat as unicorn
def project_status():
    global gl
    
    if gl == None:
        return
    
    project_dict = {}
    
    projects = gl.projects.list()
    for project in projects:
        pipelines = project.pipelines.list()
        if len(pipelines) > 0:
            lastPipeline = pipelines[1]
            project_dict[project.name.lower()] = lastPipeline.status
    
    return project_dict

