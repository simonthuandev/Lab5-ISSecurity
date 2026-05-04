import hashlib


def sha256_hash(text: str) -> str:
    """Tính SHA-256 hash của chuỗi văn bản."""
    encoded = text.encode("utf-8")
    digest = hashlib.sha256(encoded).hexdigest()
    return digest
