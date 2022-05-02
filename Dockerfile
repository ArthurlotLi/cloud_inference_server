# NOTE:
# This docker file needs to run from the folder outside! Thus, to create
# a container image, from src, run:
#
# docker build --progress plain -f cloud_inference_server/Dockerfile --tag cloud_inference_server:1.0 .

# Start with the base nvidia/cuda image to enable GPU-accelerated apps.
FROM nvidia/cuda:11.6.0-cudnn8-runtime-ubuntu18.04

# Port through which we'll expose the cloud inference server.
EXPOSE 8080

# Get python.
RUN apt-get update -y
RUN apt-get install -y python3.8
RUN apt-get install -y python3-pip
#RUN python3 -m pip install -U --force-reinstall pip
RUN python3 -m pip install --upgrade pip


# We will mimic the C:\src setup.
WORKDIR /src
COPY cloud_inference_server cloud_inference_server
RUN pip3 install -r cloud_inference_server/requirements.txt

#
# Multispeaker Synthesis
#

# Inference files
COPY multispeaker_synthesis/production_inference.py \
  multispeaker_synthesis/production_inference.py
COPY multispeaker_synthesis/production_embedding.py \
  multispeaker_synthesis/production_embedding.py

# Source folders
COPY multispeaker_synthesis/speaker_encoder \
  multispeaker_synthesis/speaker_encoder
COPY multispeaker_synthesis/synthesizer \
  multispeaker_synthesis/synthesizer
COPY multispeaker_synthesis/vocoder \
  multispeaker_synthesis/vocoder
COPY multispeaker_synthesis/utils \
  multispeaker_synthesis/utils

# Models
COPY multispeaker_synthesis/production_models/speaker_encoder/model6 \
  multispeaker_synthesis/production_models/speaker_encoder/model6
COPY multispeaker_synthesis/production_models/synthesizer/model6 \
  multispeaker_synthesis/production_models/synthesizer/model6
COPY multispeaker_synthesis/production_models/vocoder/model6 \
  multispeaker_synthesis/production_models/vocoder/model6

# Kotakee Companion
COPY kotakee_companion/speech_server/multispeaker_synthesis_utility \
  kotakee_companion/speech_server/multispeaker_synthesis_utility
COPY kotakee_companion/assets_audio/multispeaker_synthesis_speakers \
  kotakee_companion/assets_audio/multispeaker_synthesis_speakers

# Requirements
COPY multispeaker_synthesis/requirements.txt \
  multispeaker_synthesis/requirements.txt
RUN pip3 install -r multispeaker_synthesis/requirements.txt

#
# Machine Pianist
#

# Inference files
COPY machine_pianist/machine_pianist_inference.py \
  machine_pianist/machine_pianist_inference.py

# Source folders
COPY machine_pianist/data_processing \
  machine_pianist/data_processing
COPY machine_pianist/model \
  machine_pianist/model
COPY machine_pianist/utils \
  machine_pianist/utils

# Models
COPY machine_pianist/production_models/model1 \
  machine_pianist/production_models/model1

# Kotakee Companion
COPY kotakee_companion/speech_server/piano_player \
  kotakee_companion/speech_server/piano_player

# Requirements
COPY machine_pianist/requirements.txt \
  machine_pianist/requirements.txt
RUN pip3 install -r machine_pianist/requirements.txt

#
# Additional dependencies
#

# Get Pytorch - expects CUDA. 
RUN pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu113

# Multispeaker Synthesis additional dependencies.
RUN apt-get install libsndfile1-dev -y
RUN apt-get install libasound-dev libportaudio2 libportaudiocpp0 portaudio19-dev -y
RUN pip3 install pyaudio

# Machine Pianist dependencies
RUN brew install timidity

#
# Cloud Inference Server Runtime 
#

# All done. This command runs the cloud inference server when the
# container starts up. 
WORKDIR /src/cloud_inference_server
CMD PYTHONIOENCODING=utf-8 python3 cloud_web_service.py