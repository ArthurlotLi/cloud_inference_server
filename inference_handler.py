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

from handler_definitions import inference_handler_modules, inference_handler_modules_startup
from utils.dynamic_import import dynamic_load_class
from utils.base64_encoding import encode_base64, encode_base64_list

import http

class InferenceHandler:
  def __init__(self):
    """
    On startup, set up the classes + empty dict for modules and 
    go ahead and load all modules dynamically depending on the
    contents fo the handler_definitions. 
    """
    self.module_classes = {}
    self.modules = {}
    self._load_all_modules()
    self._initialize_startup_modules()

  def _load_all_modules(self):
    """
    Dynamically load all of the specified classes. Each entry should
    be in the format of "<path>.<class_name>" The module_classes
    dict will be keyed by <class_name> - this is what endpoints should
    be pointing to (Ex) MultispeakerSynthesis)
    """
    # Reset everything just in case for some reason this is called again.
    self.module_classes = {}

    for module in inference_handler_modules:
      module_split = module.rsplit(".", 1)
      module_path = module_split[0]
      module_class_name = module_split[1]

      # Load the class. Don't allow for any sloppiness - if anything's
      # mispelled, just go belly-up. 
      loaded_class = dynamic_load_class(module_path, module_class_name)
      assert loaded_class is not None
      self.module_classes[module_class_name] = loaded_class

  def _initialize_startup_modules(self):
    """
    There is an edge case of pytorch failing to load CUDNN if tensorflow
    has been loaded first. To mitigate this, load pytorch stuff first.
    """
    for index in inference_handler_modules_startup:
      module_name = inference_handler_modules[index].rsplit(".", 1)[1]
      assert module_name in self.module_classes
      print("[INFO] Inference Handler - Loading startup module %s." % module_name)
      self.modules[module_name] = self.module_classes[module_name](
        dynamic_load_class = dynamic_load_class,
      )

  def process_response(self, args, module_name, method_name):
    """
    When a response has been extracted and deemed to be our
    jurisdiction, 
    
    Returns the response provided by the handler. 
    """
    print("[INFO] Inference Handler - Processing %s method %s request with %d args." 
      % (module_name, method_name, len(args)))
    # We'll know pretty quick if the endpoint wasn't configured right. 
    if module_name not in self.module_classes:
      print("[ERROR] Inference Handler - Received an unimplemented module %s. Request rejected." % module_name)
      return (http.HTTPStatus.INTERNAL_SERVER_ERROR, "Malconfigured endpoint - unimplemented module \"%s\"!" % module_name)

    # Instantiate the module if it's not there already. 
    if module_name not in self.modules:
      print("[INFO] Inference Handler - Loading uninitialized module %s." % module_name)
      self.modules[module_name] = self.module_classes[module_name](
        dynamic_load_class = dynamic_load_class,
      )

    # Some error checking to make sure the method even exists. 
    method_func = getattr(self.modules[module_name], method_name, None)
    if not callable(method_func):
      print("[ERROR] Inference Handler - Received an unimplemented method name %s. Request rejected." % method_name)
      return (http.HTTPStatus.INTERNAL_SERVER_ERROR, "Malconfigured endpoint - unimplemented method \"%s\"!" % method_name)
    
    # Finally, call the method. Any errors that occur from here on out
    # are reported in the method function. 
    result_code, result_content, additional_processing = method_func(**args)

    if result_code == http.HTTPStatus.OK:
      # Check if we need to do some base64 encoding. 
      if additional_processing is None:
        pass
      elif additional_processing == "encode_base64":
        result_content = encode_base64(result_content)
      elif additional_processing == "encode_base64_list":
        result_content = encode_base64_list(result_content)
      else:
        # We should not allow unknown values - possibly a typo. 
        assert(False) 
    
    return (result_code, result_content)