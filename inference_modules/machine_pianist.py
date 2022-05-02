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

  def perform_midi(self, midi: str, generate_wav: str):
    """
    Given the base64 encoded midi string, save it in a temp file and
    throw it over to the utility code. 
    """
    generate_wav = int(generate_wav) == 1

    decoded_midi_file = base64.b64decode(midi)
    new_song_file = open(machine_pianist_temp_file, "wb")
    new_song_file.write(decoded_midi_file)
    new_song_file.close()

    # Overwrite the file we just wrote. 
    temp_file = self._utility_class.perform_midi(machine_pianist_temp_file, machine_pianist_temp_file)

    if temp_file is None:
      return http.HTTPStatus.BAD_REQUEST, "Machine Pianist inference failed. Verify integrity of file.", None
    
    response = []

    with open(temp_file, "rb") as midi_file:
      # Encode the midi as a base 64 string so that it can be sent over POST.
      midi = (midi_file.read())
      response.append(midi)

    # If we are also returning a mp3 file with this request, generate
    # it from the temp file. 
    if generate_wav is True:   
      temp_file2 = temp_file+ ".wav"

      print("[INFO] Machine Pianist - Running pygame to generate wav... This is a very silly thing but the ONLY way to get good control changes.")

      """
      print("[INFO] Machine Pianist - Running TiMidity to generate wav..")
      os.system("dependencies\\TiMidity\\timidity %s -Ow -o %s" % (temp_file, temp_file2))
      """
      self.midi_to_wav(temp_file, temp_file2)

      # Load the wav as a string. 
      with open(temp_file2, "rb") as audio_file:
        # Encode the midi as a base 64 string so that it can be sent over POST.
        audio = (audio_file.read())
        response.append(audio)

      os.remove(temp_file2)
    
    os.remove(temp_file)

    return http.HTTPStatus.OK, response, "encode_base64_list"

  def midi_to_wav(self, song, wav_file):
    import pyaudio  # audio recording
    import wave     # file saving
    import pygame   # midi playback
    import os       # file listing

    #### CONFIGURATION ####

    sample_rate = 44100         # Sample rate used for WAV/MP3
    channels = 2                # Audio channels (1 = mono, 2 = stereo)
    buffer = 1024               # Audio buffer size
    input_device = 1            # Which recording device to use. On my system Stereo Mix = 1


    # Begins playback of a MIDI file
    def play_music(music_file):
      try:
        pygame.mixer.music.load(music_file)
      except pygame.error:
        print ("Couldn't play %s! (%s)" % (music_file, pygame.get_error()))
        return
          
      pygame.mixer.music.play()

    # Init pygame playback
    bitsize = -16   # unsigned 16 bit
    pygame.mixer.init(sample_rate, bitsize, channels, buffer)

    # optional volume 0 to 1.0
    pygame.mixer.music.set_volume(1.0)

    # Init pyAudio
    format = pyaudio.paInt16
    audio = pyaudio.PyAudio()

    # Create a filename with a .wav extension
    new_file = wav_file

    # Open the stream and start recording
    stream = audio.open(format=format, channels=channels, rate=sample_rate, input=True, input_device_index=input_device, frames_per_buffer=buffer)
    
    # Playback the song
    print("Playing " + song + ".mid\n")
    play_music(song)
    
    frames = []
    
    # Record frames while the song is playing
    while pygame.mixer.music.get_busy():
        frames.append(stream.read(buffer))
        
    # Stop recording
    stream.stop_stream()
    stream.close()

    # Configure wave file settings
    wave_file = wave.open(new_file, 'wb')
    wave_file.setnchannels(channels)
    wave_file.setsampwidth(audio.get_sample_size(format))
    wave_file.setframerate(sample_rate)
    
    print("Saving " + new_file)   
    
    # Write the frames to the wave file
    wave_file.writeframes(b''.join(frames))
    wave_file.close()
        
    # End PyAudio    
    audio.terminate()