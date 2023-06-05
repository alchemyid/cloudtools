import falcon
from middleware  import JSONTranslator
from exec import nodes_stop, nodes_start, ec2_start, ec2_stop, ec2_pub_address, get_ecr_auth

def handle_404(req, resp):
    data = {
        'response': 'Kembalilah ke jalan yang benar!!',
    }

    resp.status = falcon.HTTP_404
    resp.context['response'] = data

class index(object):
    def on_get(self, req, resp):
        data = {'status': 200,
                'appName': 'Cloud Tools',
                'author': 'devops@xti'
                }

        resp.status = falcon.HTTP_200
        resp.context['response'] = data

def routes() -> falcon.App:
    app = falcon.App(middleware=[
        JSONTranslator()
        
    ])

    app.add_route('/', index())
    app.add_route('/aws/eks/nodes/stop', nodes_stop())
    app.add_route('/aws/eks/nodes/start', nodes_start())
    app.add_route('/aws/ec2/nodes/stop', ec2_stop())
    app.add_route('/aws/ec2/nodes/start', ec2_start())
    app.add_route('/aws/ec2/address/pub', ec2_pub_address())
    app.add_route('/aws/ecr/credential', get_ecr_auth())
    app.add_sink(handle_404, '')
    return app