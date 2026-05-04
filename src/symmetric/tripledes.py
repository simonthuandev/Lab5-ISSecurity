from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad, unpad
import binascii

BLOCK_SIZE = 8


class TripleDESModule:
    @staticmethod
    def generate_key():
        from Crypto.Random import get_random_bytes
        key = get_random_bytes(24)
        return TripleDESModule._to_hex(DES3.adjust_key_parity(key))

    @staticmethod
    def validate_key(key_hex: str) -> bytes:
        try:
            key = binascii.unhexlify(key_hex)

            if len(key) not in [16, 24]:
                raise ValueError("Key 3DES phải 16 hoặc 24 bytes")

            return DES3.adjust_key_parity(key)

        except binascii.Error:
            raise ValueError("Key không phải hex hợp lệ")

    @staticmethod
    def encrypt(plaintext: str, key_hex: str) -> str:
        try:
            key = TripleDESModule.validate_key(key_hex)
            cipher = DES3.new(key, DES3.MODE_ECB)

            padded = pad(plaintext.encode(), BLOCK_SIZE)
            ciphertext = cipher.encrypt(padded)

            return binascii.hexlify(ciphertext).decode().upper()

        except Exception as e:
            raise ValueError(f"Lỗi mã hóa 3DES: {e}")

    @staticmethod
    def decrypt(ciphertext_hex: str, key_hex: str) -> str:
        try:
            key = TripleDESModule.validate_key(key_hex)
            cipher = DES3.new(key, DES3.MODE_ECB)

            ciphertext = binascii.unhexlify(ciphertext_hex)
            decrypted = cipher.decrypt(ciphertext)
            plaintext = unpad(decrypted, BLOCK_SIZE)

            return plaintext.decode()

        except Exception as e:
            raise ValueError(f"Lỗi giải mã 3DES: {e}")

    @staticmethod
    def _to_hex(data: bytes):
        return binascii.hexlify(data).decode().upper()