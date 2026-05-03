import hashlib

class SHA256Tool:
    
    @staticmethod
    def generate_hash(data: str) -> str:
        """
        Tạo mã băm SHA-256 từ chuỗi đầu vào.
        
        Args:
            data (str): Chuỗi văn bản cần băm.
            
        Returns:
            str: Chuỗi hexadecimal của giá trị băm SHA-256 (Digest).
        """
        if not isinstance(data, str):
            raise ValueError("Dữ liệu đầu vào phải là một chuỗi văn bản (string).")
            
        # Khởi tạo đối tượng SHA-256, chuyển đổi chuỗi thành dạng bytes bằng UTF-8 và băm
        hasher = hashlib.sha256()
        hasher.update(data.encode('utf-8'))
        
        return hasher.hexdigest()

if __name__ == "__main__":
    print("-" * 40)
    print("    CÔNG CỤ TẠO MÃ BĂM SHA-256")
    print("-" * 40)
    
    try:
        text_input = input("Nhập chuỗi văn bản cần băm: ")
        digest = SHA256Tool.generate_hash(text_input)
        print(f"\n[Kết quả SHA-256]: {digest}")
    except Exception as e:
        print(f"\nĐã xảy ra lỗi: {e}")