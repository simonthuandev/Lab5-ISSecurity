import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

class AESCrypto:
    def __init__(self):
        self.block_size = AES.block_size

    def generate_random_key(self):
        """
        Tạo ngẫu nhiên một khóa AES-256 (32 bytes) và trả về dưới dạng chuỗi Base64.
        """
        key = get_random_bytes(32)
        return base64.b64encode(key).decode('utf-8')

    def _process_user_key(self, user_password):
        """
        Chuẩn hóa khóa người dùng nhập vào thành 32 bytes bằng SHA-256.
        """
        return hashlib.sha256(user_password.encode('utf-8')).digest()

    def encrypt(self, plaintext, key_input, is_random_key=False):
        """
        Mã hóa Plaintext sử dụng AES ở chế độ CBC.
        """
        try:
            # Xác định khóa (từ base64 nếu là khóa tự sinh, hoặc băm chuỗi nếu người dùng nhập)
            if is_random_key:
                key = base64.b64decode(key_input)
            else:
                key = self._process_user_key(key_input)

            # Khởi tạo thuật toán AES chế độ CBC
            cipher = AES.new(key, AES.MODE_CBC)
            iv = cipher.iv # Initialization Vector (16 bytes)

            # Padding dữ liệu và mã hóa
            padded_data = pad(plaintext.encode('utf-8'), self.block_size)
            ciphertext = cipher.encrypt(padded_data)

            # Nối IV và Ciphertext để phục vụ cho việc giải mã sau này, sau đó encode Base64
            encrypted_data = iv + ciphertext
            return base64.b64encode(encrypted_data).decode('utf-8')
        except Exception as e:
            return f"Lỗi mã hóa: {str(e)}"

    def decrypt(self, ciphertext_b64, key_input, is_random_key=False):
        """
        Giải mã Ciphertext để lấy lại Plaintext ban đầu.
        """
        try:
            if is_random_key:
                key = base64.b64decode(key_input)
            else:
                key = self._process_user_key(key_input)

            # Decode dữ liệu từ Base64
            encrypted_data = base64.b64decode(ciphertext_b64)

            # Tách IV (16 bytes đầu) và phần Ciphertext thực sự
            iv = encrypted_data[:self.block_size]
            ciphertext = encrypted_data[self.block_size:]

            # Khởi tạo lại thuật toán để giải mã
            cipher = AES.new(key, AES.MODE_CBC, iv)
            
            # Giải mã và loại bỏ padding
            decrypted_padded_data = cipher.decrypt(ciphertext)
            plaintext = unpad(decrypted_padded_data, self.block_size)
            
            return plaintext.decode('utf-8')
        except ValueError:
            return "Lỗi: Khóa không đúng hoặc dữ liệu đã bị thay đổi!"
        except Exception as e:
            return f"Lỗi giải mã: {str(e)}"
