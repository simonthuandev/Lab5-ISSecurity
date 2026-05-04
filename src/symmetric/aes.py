from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import binascii

BLOCK_SIZE = 16


class AESModule:
    @staticmethod
    def generate_key(key_size=16):
        """
        key_size: 16, 24, 32 (AES-128, 192, 256)
        """
        if key_size not in [16, 24, 32]:
            raise ValueError("Key size phải là 16, 24 hoặc 32 bytes")

        key = get_random_bytes(key_size)
        return AESModule._to_hex(key)

    @staticmethod
    def validate_key(key_hex: str) -> bytes:
        try:
            key = binascii.unhexlify(key_hex)

            if len(key) not in [16, 24, 32]:
                raise ValueError("Key AES phải 16/24/32 bytes")

            return key

        except binascii.Error:
            raise ValueError("Key không phải hex hợp lệ")

    # ================= ECB =================
    @staticmethod
    def encrypt_ecb(plaintext: str, key_hex: str) -> str:
        try:
            key = AESModule.validate_key(key_hex)
            cipher = AES.new(key, AES.MODE_ECB)

            padded = pad(plaintext.encode(), BLOCK_SIZE)
            ciphertext = cipher.encrypt(padded)

            return binascii.hexlify(ciphertext).decode().upper()

        except Exception as e:
            raise ValueError(f"Lỗi AES ECB encrypt: {e}")

    @staticmethod
    def decrypt_ecb(ciphertext_hex: str, key_hex: str) -> str:
        try:
            key = AESModule.validate_key(key_hex)
            cipher = AES.new(key, AES.MODE_ECB)

            ciphertext = binascii.unhexlify(ciphertext_hex)
            decrypted = cipher.decrypt(ciphertext)
            plaintext = unpad(decrypted, BLOCK_SIZE)

            return plaintext.decode()

        except Exception as e:
            raise ValueError(f"Lỗi AES ECB decrypt: {e}")

    # ================= CBC =================
    @staticmethod
    def encrypt_cbc(plaintext: str, key_hex: str):
        """
        Trả về: (ciphertext_hex, iv_hex)
        """
        try:
            key = AESModule.validate_key(key_hex)
            iv = get_random_bytes(16)

            cipher = AES.new(key, AES.MODE_CBC, iv)

            padded = pad(plaintext.encode(), BLOCK_SIZE)
            ciphertext = cipher.encrypt(padded)

            return (
                binascii.hexlify(ciphertext).decode().upper(),
                binascii.hexlify(iv).decode().upper()
            )

        except Exception as e:
            raise ValueError(f"Lỗi AES CBC encrypt: {e}")

    @staticmethod
    def decrypt_cbc(ciphertext_hex: str, key_hex: str, iv_hex: str) -> str:
        try:
            key = AESModule.validate_key(key_hex)
            iv = binascii.unhexlify(iv_hex)

            if len(iv) != 16:
                raise ValueError("IV phải 16 bytes")

            cipher = AES.new(key, AES.MODE_CBC, iv)

            ciphertext = binascii.unhexlify(ciphertext_hex)
            decrypted = cipher.decrypt(ciphertext)
            plaintext = unpad(decrypted, BLOCK_SIZE)

            return plaintext.decode()

        except Exception as e:
            raise ValueError(f"Lỗi AES CBC decrypt: {e}")

    # ================= helper =================
    @staticmethod
    def _to_hex(data: bytes):
        return binascii.hexlify(data).decode().upper()