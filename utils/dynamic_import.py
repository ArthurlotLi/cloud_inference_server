#
# dynamic_import.py
#
# Allows classes to import modules dynamically at runtime without having
# to update pesky files. 

import sys

def dynamic_load_class(module_name, class_name):
  """
  Dynamic class import. Changes sys.path to navigate directories
  if necessary. 
  
  Expects module_name Ex) ./home_automation/home_automation
  and class_name Ex) HomeAutomation
  """
  module = None
  imported_class = None
  module_file_name = None

  # Ex) ./home_automation - split by last slash. 
  # Don't bother if the original file is not within a subdirectory.
  split_module_name = module_name.rsplit("/", 1)
  module_folder_path = split_module_name[0]
  if(module_folder_path != "." and len(split_module_name) > 1):
    sys.path.append(module_folder_path)
    module_file_name = split_module_name[1]
  else:
    module_file_name = module_name.replace("./", "")

  # Fetch the module first.
  try:
    module = __import__(module_file_name)
  except:
    print("[ERROR] Failed to import module " + module_file_name + " from subdirectory '" + module_folder_path + "'.")
    return None

  # Return the class. 
  try:
    imported_class = getattr(module, class_name)
  except:
    print("[ERROR] Failed to import class_name " + class_name + ".")
    return None

  return imported_class