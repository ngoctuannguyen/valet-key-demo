import hashlib
import hmac
import time
import base64
import urllib.parse

SECRET_KEY = "eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4"  # Replace this with a strong, secure key

def generate_valet_key_url(file_path, expiry_in_seconds=60):
    # Expiration time in the future
    expiry_time = int(time.time()) + expiry_in_seconds

    # Create a message combining the document_id and expiry_time
    message = f"{file_path}:{expiry_time}"

    # Generate an HMAC signature with the secret key
    signature = hmac.new(SECRET_KEY.encode(), message.encode(), hashlib.sha256).hexdigest()

    # Encode the URL with parameters
    query_params = urllib.parse.urlencode({
        "file_path": file_path,
        "expiry": expiry_time,
        "signature": signature
    })

    return query_params
