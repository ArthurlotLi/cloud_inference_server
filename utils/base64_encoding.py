#
# base64_encoding.py
#
# Allows for transmission of files over the wire to our clients, as
# well as receipt of them. 

import base64
import time

def encode_base64_list(list):
  """ 
  As opposed to the others, takes in a list. Will result in a JSON
  friendly dict with numbered indices. 
  """
  start_time = time.time()
  encoded_dict = {}
  total_len = 0
  for i in range(0, len(list)):
    encoded_dict[i] = str(base64.b64encode(list[i]), "utf-8")
    total_len += len(list[i])
  print("[DEBUG] Base64 - Encoding string of unencoded len %d took %.2f seconds." % (total_len, time.time()-start_time))
  return encoded_dict

def encode_base64(string):
  start_time = time.time()
  encoded_string = str(base64.b64encode(string), "utf-8")
  print("[DEBUG] Base64 - Encoding string of unencoded len %d took %.2f seconds." % (len(string), time.time()-start_time))
  return encoded_string

def decode_base64(string):
  start_time = time.time()
  decoded_string = str(base64.b64decode(string), "utf-8")
  print("[DEBUG] Base64 - Decoding base64 string of unencoded len %d took %.2f seconds." % (len(decoded_string), time.time()-start_time))
  return decoded_string