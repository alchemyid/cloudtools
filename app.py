import falcon
from routes import routes

def http() -> falcon.App():
    return routes()
