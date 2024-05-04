import hashlib


def get_hash_sig(file: str) -> str:
    BLOCK = 1048576  # 1MB
    sha256 = hashlib.sha256()
    with open(file, 'rb') as f:
        buf = f.read(BLOCK)
        while buf:
            sha256.update(buf)
            buf = f.read(BLOCK)
    return sha256.hexdigest()
