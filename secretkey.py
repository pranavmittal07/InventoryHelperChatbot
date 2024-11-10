import os
import base64

secret_key = os.urandom(24)
secret_key_base64 = base64.b64encode(secret_key).decode('utf-8')

print("Secret Key (Base64):", secret_key_base64)
