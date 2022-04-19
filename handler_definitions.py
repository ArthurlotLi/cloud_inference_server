#
# handler_definitions.py
#
# For all handlers, define the classes that you will be supporting. 

inference_handler_modules = [
  "./inference_modules/multispeaker_synthesis.MultispeakerSynthesis",
  "./inference_modules/machine_pianist.MachinePianist",
]

# Indices of modules to load on startup. 
inference_handler_modules_startup = [0]