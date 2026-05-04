from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import binascii

BLOCK_SIZE = 8


class DESModule:
    @staticmethod
    def generate_key():
        return DESModule._to_hex(DESModule._random_bytes(8))

    @staticmethod
    def validate_key(key_hex: str) -> bytes:
        try:
            key = binascii.unhexlify(key_hex)
            if len(key) != 8:
                raise ValueError("Key phải 8 bytes (16 ký tự hex)")
            return key
        except binascii.Error:
            raise ValueError("Key không phải hex hợp lệ")

    @staticmethod
    def encrypt(plaintext: str, key_hex: str) -> str:
        try:
            key = DESModule.validate_key(key_hex)
            cipher = DES.new(key, DES.MODE_ECB)

            padded = pad(plaintext.encode(), BLOCK_SIZE)
            ciphertext = cipher.encrypt(padded)

            return binascii.hexlify(ciphertext).decode().upper()

        except Exception as e:
            raise ValueError(f"Lỗi mã hóa DES: {e}")

    @staticmethod
    def decrypt(ciphertext_hex: str, key_hex: str) -> str:
        try:
            key = DESModule.validate_key(key_hex)
            cipher = DES.new(key, DES.MODE_ECB)

            ciphertext = binascii.unhexlify(ciphertext_hex)
            decrypted = cipher.decrypt(ciphertext)
            plaintext = unpad(decrypted, BLOCK_SIZE)

            return plaintext.decode()

        except Exception as e:
            raise ValueError(f"Lỗi giải mã DES: {e}")

    # helper
    @staticmethod
    def _random_bytes(n):
        from Crypto.Random import get_random_bytes
        return get_random_bytes(n)

    @staticmethod
    def _to_hex(data: bytes):
        return binascii.hexlify(data).decode().upper()