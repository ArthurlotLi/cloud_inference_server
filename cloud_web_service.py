#
# cloud_web_service.py
#
# Component in charge of interacting with clients, serving endpoints
# defined by endpoint_distributions.py. Depending on the endpoint,
# forwards requests to the appropriate handler. 

from service_definitions import *

from flask import Flask
from flask_restful import Resource, Api, reqparse

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
    def post(self):
      parser = reqparse.RequestParser()
      parser.add_argument("speaker_id")
      parser.add_argument("text")
      args = parser.parse_args()

      response_code, content = endpoints["synthesizeText"].process_response(args)

      return content, response_code

    endpoint_class = type(endpoint_name, (Resource,), {
      "post": post,
    })
    api.add_resource(endpoint_class, '/%s' % endpoint_name)

if __name__ == "__main__":
  define_endpoints()
  app.run(debug = False, host=service_host, port = service_port)