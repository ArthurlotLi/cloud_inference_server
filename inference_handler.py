#
# inference_handler.py
#
# Handler in charge of on-demand requests for machine learning 
# inference. Manages a module list that is kept clean according to
# the timouts of individual modules. Frequently used modules are 
# kept in memory. 
#
# For every request, either returns a tuple of the response code and
# the processed result or an error message. For many cases, the 
# processed result is a base64 encoded string ready for return. 

class InferenceHandler:
  def __init__(self):
    self.modules = {}

  def process_response(self, args, module_name):
    """
    When a response has been extracted and deemed to be our
    jurisdiction, 
    Returns the response provided by the handler. 
    """

    invert_op = getattr(self, module_name, None)
    if not callable(invert_op):
      print("[ERROR] Inference Handler - Received an unimplemented module %s. Request rejected." % module_name)
      return (False, "Malconfigured endpoint - unimplemented module \"%s\"!" % module_name)