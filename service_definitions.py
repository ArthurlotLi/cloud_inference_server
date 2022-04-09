#
# service_definitions.py
#
# Declaration of endpoints for the cloud_web_service to use. Each item
# should indicate information about the endpoint itself as well as what
# handler + handler module should be responsible for serving a response. 

from service_objects import *
from inference_handler import *

inference_handler = 

endpoints = {
  "synthesizeText": CloudEndpoint(
      url_args = ["speaker_id", "model_id", "text"]
      handler 
    ),
}