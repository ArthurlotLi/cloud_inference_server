# NOTE:
# This docker file needs to run in the folder outside! Thus, to create
# a container image, first copy the dockerfile into src and then, from
# src, run:
#
# docker build -f cloud_inference_server/Dockerfile --tag cloud_inference_server:1.0 .

# Start with a base python image.
FROM python:3.8

# Change the port if necessary.
EXPOSE 8080

# We will mimic the C:\src setup.
WORKDIR /src
COPY cloud_inference_server cloud_inference_server
RUN pip install -r cloud_inference_server/requirements.txt

# Append additional repositories as necessary.
COPY multispeaker_synthesis multispeaker_synthesis
RUN pip install -r multispeaker_synthesis/requirements.txt

COPY machine_pianist machine_pianist
RUN pip install -r machine_pianist/requirements.txt

# Grab only the speech_server utilities that we'll need. Append more
# As you add more repositories. 
COPY kotakee_companion/speech_server/multispeaker_synthesis_utility \
  kotakee_companion/speech_server/multispeaker_synthesis_utility
COPY kotakee_companion/assets_audio/multispeaker_synthesis_speakers \
  kotakee_companion/assets_audio/multispeaker_synthesis_speakers

COPY kotakee_companion/speech_server/piano_player \
  kotakee_companion/speech_server/piano_player

# Get Pytorch - expects CUDA. 
RUN pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu113

# Multispeaker Synthesis
RUN apt-get update
RUN apt-get install libsndfile1-dev -y
RUN apt-get install libasound-dev libportaudio2 libportaudiocpp0 portaudio19-dev -y
RUN pip install pyaudio
# All done. This command runs the cloud inference server when the
# container starts up. 
WORKDIR /src/cloud_inference_server
CMD python cloud_web_service.py


