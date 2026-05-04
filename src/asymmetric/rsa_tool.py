import base64
import json
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


def generate_keys():
    key = RSA.generate(2048)

    private_key = key.export_key().decode()
    public_key = key.publickey().export_key().decode()

    print("\n===== RSA Key Pair Generated =====")
    print("\n Public Key:\n")
    print(public_key)
    print("\n Private Key:\n")
    print(private_key)

    return public_key, private_key


def encrypt_text(plaintext, key_str):
    key = RSA.import_key(key_str)
    cipher = PKCS1_OAEP.new(key)

    ciphertext = cipher.encrypt(plaintext.encode())
    ciphertext_b64 = base64.b64encode(ciphertext).decode()

    print("\n Ciphertext:\n")
    print(ciphertext_b64)
    return ciphertext_b64


def decrypt_text(ciphertext_b64, key_str):
    key = RSA.import_key(key_str)
    cipher = PKCS1_OAEP.new(key)

    ciphertext = base64.b64decode(ciphertext_b64)
    plaintext = cipher.decrypt(ciphertext).decode()

    print("\n Plaintext:\n")
    print(plaintext)
    return plaintext


def main():
    public_key = None
    private_key = None

    while True:
        print("\n===== RSA Encryption Tool =====")
        print("1. Generate RSA Key Pair")
        print("2. Encrypt Text")
        print("3. Decrypt Text")
        print("4. Exit")

        choice = input("Your choice: ")

        if choice == "1":
            public_key, private_key = generate_keys()

        elif choice == "2":
            if public_key is None:
                print(" You must generate keys first!")
                continue

            plaintext = input("Nhập plaintext: ")
            print("Mã hóa bằng key nào?")
            print("1. Public Key")
            print("2. Private Key")
            key_choice = input("Your choice: ")

            if key_choice == "1":
                encrypt_text(plaintext, public_key)
            else:
                encrypt_text(plaintext, private_key)

        elif choice == "3":
            if private_key is None:
                print(" You must generate keys first!")
                continue

            ciphertext = input("Nhập ciphertext: ")
            print("Giải mã bằng key nào?")
            print("1. Private Key")
            print("2. Public Key")
            key_choice = input("Your choice: ")

            if key_choice == "1":
                decrypt_text(ciphertext, private_key)
            else:
                decrypt_text(ciphertext, public_key)

        elif choice == "4":
            print("Bye!")
            break

        else:
            print("Invalid choice, try again!")


if __name__ == "__main__":
    main()