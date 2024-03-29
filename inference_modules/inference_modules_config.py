#
# inference_modules_config.py
#
# Master place to dump all configuration for all modules used for
# inference (model numbers, locations, etc).

multispeaker_synthesis_model_num = "model6"
multispeaker_synthesis_inference_location = "../multispeaker_synthesis/production_inference"
multispeaker_synthesis_inference_class_name = "MultispeakerSynthesis"
multispeaker_synthesis_models_location = "../multispeaker_synthesis/production_models"
multispeaker_synthesis_speakers_location = "../kotakee_companion/assets_audio/multispeaker_synthesis_speakers"
multispeaker_synthesis_kotakee_utility = "../kotakee_companion/speech_server/multispeaker_synthesis_utility/multispeaker_synthesis_utility"
multispeaker_synthesis_kotakee_utility_class = "MultispeakerSynthesisUtility"

machine_pianist_kotakee_utility = "../kotakee_companion/speech_server/piano_player/machine_pianist_utility"
machine_pianist_kotakee_utility_class = "MachinePianistUtility"
machine_pianist_model_path = "../machine_pianist/production_models/model6/machine_pianist.h5"
machine_pianist_scaler_X_path = "../machine_pianist/saved_models/model6_scaler_X.bin"
machine_pianist_scaler_Y_path = "../machine_pianist/saved_models/model6_scaler_Y.bin"
machine_pianist_inference_folder = "../machine_pianist/machine_pianist_inference"
machine_pianist_inference_class = "MachinePianist"
machine_pianist_temp_file = "temp_file_midi"