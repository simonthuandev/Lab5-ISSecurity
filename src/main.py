from symmetric.aes import AESModule
from symmetric.des import DESModule
from symmetric.tripledes import TripleDESModule
if __name__ == "__main__":
    key = AESModule.generate_key(16)

    text = "hello AES"

    # ECB
    enc = AESModule.encrypt_ecb(text, key)
    print("ECB:", enc)
    print("DEC:", AESModule.decrypt_ecb(enc, key))

    # CBC
    enc, iv = AESModule.encrypt_cbc(text, key)
    print("CBC:", enc)
    print("IV :", iv)
    print("DEC:", AESModule.decrypt_cbc(enc, key, iv))