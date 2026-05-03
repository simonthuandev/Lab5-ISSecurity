import hashlib


def sha256_hash(text):
    """
    Calculate the SHA-256 hash of the given text.

    Args:
        text (str): The input text to hash.

    Returns:
        str: The SHA-256 hash of the input text.
    """
    if not text.strip():
        raise ValueError("input cannot be empty!")
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
