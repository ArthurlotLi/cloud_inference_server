#
# machine_pianist.py
#
# Interfacing with the Machine Pianist project. Allows for remote
# clients to request performances given trained models augmenting
# midi files with human-like performance data. 
#
# As a reminder, every single method supported by handlers must
# return a tuple, with [0] = HTTP code and [1] = content (or error
# message), and [2] = key for whatever postprocessing you need
# (Ex) "encode_base64")

from inference_modules_config import *

import os
import http
import base64

class MachinePianist:
  def __init__(self, dynamic_load_class):
    """
    On startup. Load the machine pianist into memory, with all of this
    being done by the kotakee companion utility code.
    """
    print("[INFO] Machine Pianist - Loading model at: %s." 
      % machine_pianist_model_path)

    # Now go ahead and load the kotakee companion files that we'll
    # be using. This is to avoid duplicate code and increase 
    # simplicity of implementation. 
    self._utility_class_type = dynamic_load_class(module_name=machine_pianist_kotakee_utility, 
                                            class_name=machine_pianist_kotakee_utility_class)
    assert self._utility_class_type is not None
    self._utility_class = self._utility_class_type(model_path=machine_pianist_model_path,
                                                  inference_folder=machine_pianist_inference_folder,
                                                   inference_class= machine_pianist_inference_class)

  def perform_midi(self, midi: str):
    """
    Given the base64 encoded midi string, save it in a temp file and
    throw it over to the utility code. 
    """
    decoded_midi_file = base64.b64decode(midi)
    new_song_file = open(machine_pianist_temp_file, "wb")
    new_song_file.write(decoded_midi_file)
    new_song_file.close()

    # Overwrite the file we just wrote. 
    temp_file = self._utility_class.perform_midi(machine_pianist_temp_file, machine_pianist_temp_file)

    if temp_file is None:
      return http.HTTPStatus.BAD_REQUEST, "Machine Pianist inference failed. Verify integrity of file.", None
    
    with open(temp_file, "rb") as midi_file:
      # Encode the midi as a base 64 string so that it can be sent over POST.
      encoded_midi_file = base64.b64encode(midi_file.read())
    
    os.remove(temp_file)

    return http.HTTPStatus.OK, encoded_midi_file, "encode_base64"