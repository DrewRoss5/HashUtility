import hashlib
import base64

def hash_file(file_path: str):
    digest = hashlib.sha256()
    with open(file_path, 'rb') as f:
        digest.update(f.read())
    file_hash = digest.digest()
    return base64.b64encode(file_hash).decode()