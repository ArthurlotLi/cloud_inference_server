#
# base64_encoding.py
#
# Allows for transmission of files over the wire to our clients, as
# well as receipt of them. 

import base64
import time

def encode_base64(string):
  start_time = time.time()
  encoded_string = base64.b64encode(string)
  print("[DEBUG] Base64 - Encoding string of unencoded len %d took %.2f seconds." % (len(string), time.time()-start_time))
  return encoded_string

def decode_base64(string):
  start_time = time.time()
  decoded_string = base64.b64decode(string)
  print("[DEBUG] Base64 - Decoding base64 string of unencoded len %d took %.2f seconds." % (len(decoded_string), time.time()-start_time))
  return decoded_string