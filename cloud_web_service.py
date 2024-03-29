#
# cloud_web_service.py
#
# Component in charge of interacting with clients, serving endpoints
# defined by endpoint_distributions.py. Depending on the endpoint,
# forwards requests to the appropriate handler. 

from service_definitions import *

from flask import Flask
from flask_restful import Resource, Api, reqparse
#from gevent.pywsgi import WSGIServer
#from gevent.pool import Pool
import eventlet
from eventlet import wsgi

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
      """
      Parses all arguments as Unicode strings. 
      """
      parser = reqparse.RequestParser()
      for arg in endpoints[endpoint_name].url_args:
        parser.add_argument(arg, type=str)
      args = parser.parse_args()
      response_code, content = endpoints[endpoint_name].process_response(args)
      return content, response_code

    endpoint_class = type(endpoint_name, (Resource,), {
      "post": post,
    })
    api.add_resource(endpoint_class, '/%s' % endpoint_name)

# Define endpoints now. 
define_endpoints()

if __name__ == "__main__":
  # NOTE: Obsolete, as Python Flask is not a production web server.
  # It can only handle one request as a time. This led to some requests
  # spontaneously failing, timing out, etc.
  #app.run(
    #threaded = service_threading, 
    #debug = False, 
    #host=service_host, 
    #port = service_port)

  # Use WSGIServer instead. 
  #print("[INFO] Cloud Inference - Server is now online at http://%s:%d." % (service_host, service_port))
  #pool = Pool()
  #app.debug = False 
  #http_server = WSGIServer((service_host, service_port), app, spawn=pool)
  #http_server.serve_forever()

  print("[INFO] Cloud Inference - Server is now online at http://%s:%d." % (service_host, service_port))
  app.debug = False 
  try:
    http_server = wsgi.server(eventlet.listen((service_host, service_port)),  app)
  except Exception as e:
    print("[ERROR] Cloud Inference - Server error! Exception:")
    print(e)