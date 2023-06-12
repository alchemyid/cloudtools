from helpers import helpers
import falcon
import json
import os
import time


class get_ecr_auth(object):
    def on_post(self, req, resp):
        try:
            raw = req.context['request']
            os.environ['AWS_ACCESS_KEY_ID'] = raw['access_key']
            os.environ['AWS_SECRET_ACCESS_KEY'] = raw['secret_key']
            os.environ['AWS_DEFAULT_REGION'] = raw['region']
            
            ecr = helpers.command("aws ecr get-login-password --region "+raw["region"]+"")
            account = helpers.command("aws sts get-caller-identity --output json")
            d = json.loads(account)
            if type(ecr) is str :
                j = {
                    "user" : "AWS",
                    "password": ecr,
                    "endpoint" : d["Account"]+".dkr.ecr."+raw["region"]+".amazonaws.com"
                }
            else:
                j = ecr
            resp.status = falcon.HTTP_200
            resp.context['response'] = j
        except Exception as e:
            raise falcon.HTTPError(falcon.HTTP_404, str(e))
class nodes_stop(object):
    def on_post(self, req, resp):

        try:
            raw = req.context['request']

            os.environ['AWS_ACCESS_KEY_ID'] = raw['access_key']
            os.environ['AWS_SECRET_ACCESS_KEY'] = raw['secret_key']
            os.environ['AWS_DEFAULT_REGION'] = raw['region']

            helpers.command("aws eks update-kubeconfig --name " +raw["cluster_name"]+ "")
            
            helpers.command("kubectl scale --replicas=0 deployment/cluster-autoscaler -n kube-system")
            time.sleep(1)

            node = helpers.command("aws eks update-nodegroup-config --cluster-name "+raw["cluster_name"]+" --nodegroup-name "+raw["nodegroup_name"]+" \
                            --scaling-config minSize=0,maxSize=1,desiredSize=0")
            
            if type(node) is str :
                j = json.loads(node)
            else:
                j = node
            resp.status = falcon.HTTP_200
            resp.context['response'] = j

        except Exception as e:
            raise falcon.HTTPError(falcon.HTTP_404, str(e))

class nodes_start(object):
    def on_post(self, req, resp):

        try:
            raw = req.context['request']

            os.environ['AWS_ACCESS_KEY_ID'] = raw['access_key']
            os.environ['AWS_SECRET_ACCESS_KEY'] = raw['secret_key']
            os.environ['AWS_DEFAULT_REGION'] = raw['region']

            helpers.command("aws eks update-kubeconfig --name " +raw["cluster_name"]+ "")
            
            node = helpers.command("aws eks update-nodegroup-config --cluster-name "+raw["cluster_name"]+" --nodegroup-name "+raw["nodegroup_name"]+" \
                            --scaling-config minSize="+raw["ng_minSize"]+",maxSize="+raw["ng_maxSize"]+",desiredSize="+raw["ng_desiredSize"]+"")

            helpers.command("kubectl scale --replicas=1 deployment/cluster-autoscaler -n kube-system")
            
            if type(node) is str :
                j = json.loads(node)
            else:
                j = node
            resp.status = falcon.HTTP_200
            resp.context['response'] = j

        except Exception as e:
            raise falcon.HTTPError(falcon.HTTP_404, str(e))

class ec2_start(object):
    def on_post(self, req, resp):

        try:
            raw = req.context['request']

            os.environ['AWS_ACCESS_KEY_ID'] = raw['access_key']
            os.environ['AWS_SECRET_ACCESS_KEY'] = raw['secret_key']
            os.environ['AWS_DEFAULT_REGION'] = raw['region']

            ec2 = raw["ec2"]
            # ids = []
            # for x in json.loads(nodes):
            #     filter = "Name=private-dns-name,Values="+x+""
            #     instanceId = helpers.command("aws ec2 describe-instances --filters "+filter+" --query 'Reservations[].Instances[].[InstanceId]' --output text")
            #     ids.append(instanceId)
            
            join = ' '.join(str(e) for e in ec2)
            e = helpers.command("aws ec2 start-instances --instance-ids "+join+"")
            
            if type(e) is str :
                j = json.loads(e)
            else:
                j = e
            resp.status = falcon.HTTP_200
            resp.context['response'] = j

        except Exception as e:
            raise falcon.HTTPError(falcon.HTTP_404, str(e))

class ec2_stop(object):
    def on_post(self, req, resp):

        try:
            raw = req.context['request']

            os.environ['AWS_ACCESS_KEY_ID'] = raw['access_key']
            os.environ['AWS_SECRET_ACCESS_KEY'] = raw['secret_key']
            os.environ['AWS_DEFAULT_REGION'] = raw['region']

            ec2 = raw["ec2"]
            join = ' '.join(str(e) for e in ec2)
            e = helpers.command("aws ec2 stop-instances --instance-ids "+join+"")
            
            if type(e) is str :
                j = json.loads(e)
            else:
                j = e
            resp.status = falcon.HTTP_200
            resp.context['response'] = j
            
        except Exception as e:
            raise falcon.HTTPError(falcon.HTTP_404, str(e))

class ec2_pub_address(object):
    def on_post(self, req, resp):

        try:
            raw = req.context['request']

            os.environ['AWS_ACCESS_KEY_ID'] = raw['access_key']
            os.environ['AWS_SECRET_ACCESS_KEY'] = raw['secret_key']
            os.environ['AWS_DEFAULT_REGION'] = raw['region']
            filter = "Name=instance-id,Values="+raw["instance-id"]+""
            ip = helpers.command("aws ec2 describe-instances --filters "+filter+" --query 'Reservations[].Instances[].[PublicIpAddress]' --output json")
            
            if type(ip) is str :
                j = json.loads(ip)
            else:
                j = ip
            resp.status = falcon.HTTP_200
            resp.context['response'] = j
            
        except Exception as e:
            raise falcon.HTTPError(falcon.HTTP_404, str(e))
        

