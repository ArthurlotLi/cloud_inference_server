#
# cloud_web_service.py
#
# Component in charge of interacting with clients, serving endpoints
# defined by endpoint_distributions.py. Depending on the endpoint,
# forwards requests to the appropriate handler. 

from service_definitions import *

from flask import Flask
from flask_restful import Resource, Api, reqparse
from gevent.pywsgi import WSGIServer

# Define the application.
app = Flask(__name__)

# Define the API, which we will add our endpoints onto. 
api = Api(app)

# Define a basic entry point API for heartbeats. 
class BasicEndpoint(Resource):
  def get(self):
    return {}
api.add_resource(BasicEndpoint, "/")

def define_endpoints():
  """
  Given all the endpoints present in service_definitions, generate
  flask restful resources. 
  """
  for endpoint_name in endpoints:
    # Shove in the stuff we need as defaults. Feels very hacky... but
    # it works! 
    def post(self, endpoint_name = endpoint_name, endpoints = endpoints):
      parser = reqparse.RequestParser()
      for arg in endpoints[endpoint_name].url_args:
        parser.add_argument(arg)
      args = parser.parse_args()
      response_code, content = endpoints[endpoint_name].process_response(args)
      return content, response_code

    endpoint_class = type(endpoint_name, (Resource,), {
      "post": post,
    })
    api.add_resource(endpoint_class, '/%s' % endpoint_name)

if __name__ == "__main__":
  define_endpoints()

  # NOTE: Obsolete, as Python Flask is not a production web server.
  # It can only handle one request as a time. This led to some requests
  # spontaneously failing, timing out, etc.
  #app.run(
    #threaded = service_threading, 
    #debug = False, 
    #host=service_host, 
    #port = service_port)

  # Use WSGIServer instead. 
  print("[INFO] Cloud Inference - Server is now online at http://%s:%d." % (service_host, service_port))
  app.debug = True 
  http_server = WSGIServer((service_host, service_port), app)
  http_server.serve_forever()