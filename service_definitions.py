#
# service_definitions.py
#
# Declaration of endpoints for the cloud_web_service to use. Each item
# should indicate information about the endpoint itself as well as what
# handler + handler module should be responsible for serving a response. 

from service_objects import *
from inference_handler import *

service_host = '0.0.0.0'
service_port = 9121
service_threading = True

inference_handler = InferenceHandler()

endpoints = {
  "synthesizeText": CloudEndpoint(
      url_args = ["speaker_id", "text"],
      handler = inference_handler,
      module_name = "MultispeakerSynthesis",
      method_name = "synthesize_text",
    ),
  "performMidi": CloudEndpoint(
      url_args = ["midi", "generate_wav", "filename"],
      handler = inference_handler,
      module_name = "MachinePianist",
      method_name = "perform_midi",
    ),
}