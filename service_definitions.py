#
# service_definitions.py
#
# Declaration of endpoints for the cloud_web_service to use. Each item
# should indicate information about the endpoint itself as well as what
# handler + handler module should be responsible for serving a response. 

from service_objects import *
from inference_handler import *

service_host = '192.168.0.108'
service_port = 8080

inference_handler = InferenceHandler()

endpoints = {
  "synthesizeText": CloudEndpoint(
      url_args = ["speaker_id", "text"],
      handler = inference_handler,
      module_name = "MultispeakerSynthesis",
      method_name = "synthesize_text",
    ),
}