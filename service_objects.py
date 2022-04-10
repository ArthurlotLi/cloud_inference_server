#
# service_objects.py
#
# Classes encompassing all general interactions of the cloud inference
# server. 

class CloudEndpoint:
  def __init__(self, url_args, handler, module_name, method_name):
    """
    Require the list of url args (if any), the instantiated handler 
    class, as well as the name of the module of the handler to use.
    """
    self.url_args = url_args
    self.handler = handler
    self.module_name = module_name
    self.method_name = method_name
  
  def process_response(self, args):
    """
    When a valid endpoint has been attained, immediately parse the
    arguments and stuff it into the handler's jurisdiction.

    Returns the response provided by the handler. 
    """
    print("[INFO] Cloud Endpoint - %s - %s request received. Processing..." % (self.module_name, self.method_name))
    response_code, content = self.handler.process_response(
      args = args,
      module_name = self.module_name,
      method_name = self.method_name
    )

    return response_code, content

