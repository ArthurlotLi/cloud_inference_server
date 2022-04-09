#
# inference_multispeaker_synthesis.py
#
# Module for interfacing with MultispeakerSynthesis. All dependencies
# for MultispeakerSynthesis must have been properly installed first,
# with the multispeaker_synthesis repo having been placed adjacent
# to the cloud_inference_server code. Don't forget to add the model!
#
# As a reminder, every single method supported by handlers must
# return a tuple, with [0] = HTTP code and [1] = content (or error
# message), and [2] = key for whatever postprocessing you need
# (Ex) "encode_base64")

from inference_modules_config import *

import http

class MultispeakerSynthesis:
  # Given model variants location, how do we get to synthesizer models? 
  _model_variants_synthesizer_subpath = "synthesizer"
  _model_suffix = ".pt"

  def __init__(self, dynamic_load_class):
    """
    On startup, load the synthesizer into memory in anticipation of
    incoming requests. 
    """
    print("[DEBUG] MultispeakerSynthesis - Initializing model variant "+str(multispeaker_synthesis_model_num)+"...")

    # Now go ahead and load the kotakee companion files that we'll
    # be using. This is to avoid duplicate code and increase 
    # simplicity of implementation. 
    self._utility_class_type = dynamic_load_class(module_name=multispeaker_synthesis_kotakee_utility, 
                                            class_name=multispeaker_synthesis_kotakee_utility_class)
    assert self._utility_class_type is not None
    self._utility_class = self._utility_class_type(
      model_num = multispeaker_synthesis_model_num, 
      model_variants_location = multispeaker_synthesis_models_location, 
      speakers_location = multispeaker_synthesis_speakers_location, 
      inference_location = multispeaker_synthesis_inference_location, 
      inference_class_name = multispeaker_synthesis_inference_class_name
    )

  def synthesize_text(self, speaker_id, text):
    """
    Given the speaker id and the text in one large string, go and 
    synthesize a wav and provide that back to the handler, who will
    encode it in base64 to be consumed by users. 
    """
    # Use the utility to manage everything. We will get an array of
    # wavs back. 
    wavs = self._utility_class.speaker_synthesize_speech(texts=[text], speaker_id=speaker_id, utterance_id="")
    if wavs is None or len(wavs) == 0:
      return http.HTTPStatus.BAD_REQUEST, "Speech Synthesis failed. Please verify speaker id.", None

    return http.HTTPStatus.OK, wavs, "encode_base64_list"