import hashlib


def sha256_hash(text):
    """Tính SHA-256 hash của chuỗi văn bản."""
    if not text.strip():
        raise ValueError("input cannot be empty!")
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
