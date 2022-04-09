#
# cloud_web_service.py
#
# Component in charge of interacting with clients, serving endpoints
# defined by endpoint_distributions.py. Depending on the endpoint,
# forwards requests to the appropriate handler. 

from service_definitions import *

if __name__ == "__main__":
  args = {
    "speaker_id": "ELEANOR",
    "model_id": "model6",
    "text":"Hello world from Kotakee Companion",
  }
  query = ""
  endpoints["synthesizeText"].process_response(query)