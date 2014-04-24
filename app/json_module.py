"""
The JSON encoding/decoding

Abstracted into its own module in case that we want to change the
implementation later on.
"""

import json

json_encode = json.JSONEncoder().encode
json_decode = json.JSONDecoder().decode


