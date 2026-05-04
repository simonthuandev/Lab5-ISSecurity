from core.input_handler import (
    prompt, prompt_menu, prompt_encrypt_or_decrypt,
    NavigateBack, NavigateMain, NavigateQuit,
)
from core.output_handler import (
    print_section, print_result_box, print_key_box,
    print_error, print_warning, print_info, show_result_actions,
)
from symmetric.aes import AESCrypto
from symmetric.des import DESModule
from symmetric.tripledes import TripleDESModule


# ─────────────────────────────────────────────────────────────────────────────
def _prompt_hex_key(
    key_label: str,
    generator_fn,
    key_hint: str = "",
    allow_generate: bool = True,
) -> str:
    options = {"1": f"Tự nhập {key_label}"}
    if allow_generate:
        options["2"] = f"Tự động tạo {key_label} ngẫu nhiên"
    choice = prompt_menu(options, f"Quản lý {key_label}")

    if allow_generate and choice == "2":
        key_hex = generator_fn()
        print_key_box(f"{key_label} (HEX)", key_hex)
        return key_hex

    if key_hint:
        print_info(key_hint)
    return prompt(f"Nhập {key_label}: ")


def _prompt_aes_key(aes_tool: AESCrypto, action: str) -> tuple[str, bool]:
    if action == "encrypt":
        options = {
            "1": "Tạo mật khẩu thủ công (được SHA-256 thành key AES-256)",
            "2": "Nhập khóa random AES-256 (Base64)",
            "3": "Tạo khóa random AES-256 mới (Base64)",
        }
    else:
        options = {
            "1": "Nhập mật khẩu thủ công đã tạo",
            "2": "Nhập khóa random AES-256 (Base64)",
        }
    choice = prompt_menu(options, "Quản lý khóa AES")

    if choice == "1":
        return prompt("Nhập mật khẩu AES: "), False
    if choice == "2":
        return prompt("Nhập khóa random AES (Base64): "), True

    if action != "encrypt":
        raise ValueError("Lựa chọn không hợp lệ cho bước giải mã AES.")

    random_key_b64 = aes_tool.generate_random_key()
    print_key_box("Khóa AES random (Base64)", random_key_b64)
    print_info("Lưu lại khóa này để có thể giải mã đúng dữ liệu đã mã hóa.")
    return random_key_b64, True

def _aes_flow() -> str:
    print_section("🔷 AES (Advanced Encryption Standard)")
    print_info("Chế độ hỗ trợ: CBC")

    step = 1
    action = key_input = None
    is_random_key = False
    aes_tool = AESCrypto()

    while True:
        try:
            if step == 1:
                action = prompt_encrypt_or_decrypt()
                step = 2

            elif step == 2:
                key_input, is_random_key = _prompt_aes_key(aes_tool, action)
                step = 3

            elif step == 3:
                try:
                    if action == "encrypt":
                        plaintext = prompt("Nhập văn bản cần mã hóa: ")
                        result = aes_tool.encrypt(plaintext, key_input, is_random_key=is_random_key)
                        if result.startswith("Lỗi"):
                            raise ValueError(result)
                        print_result_box("Ciphertext (Base64)", result)
                        return show_result_actions(result)
                    else:
                        ct = prompt("Nhập Ciphertext (Base64): ")
                        result = aes_tool.decrypt(ct, key_input, is_random_key=is_random_key)
                        if result.startswith("Lỗi"):
                            raise ValueError(result)
                        print_result_box("Plaintext (kết quả giải mã)", result)
                        return show_result_actions(result)
                except (NavigateBack, NavigateMain, NavigateQuit):
                    raise
                except Exception as e:
                    print_error(str(e))
                    return "R"

        except NavigateBack:
            if step > 1:
                step -= 1   # lùi về bước trước
            else:
                return "B"  # bước 1 → báo cho caller quay về menu thuật toán

        except NavigateMain:
            return "M"

        except NavigateQuit:
            return "Q"


def _des_flow() -> str:
    print_section("🔷 DES (Data Encryption Standard)")
    print_warning("DES không còn an toàn — chỉ dùng cho mục đích giáo dục!")
    print_info("Khóa: 8 bytes (16 ký tự HEX) | Chế độ hỗ trợ: ECB")

    step = 1
    action = key = None

    while True:
        try:
            if step == 1:
                action = prompt_encrypt_or_decrypt()
                step = 2

            elif step == 2:
                key = _prompt_hex_key(
                    "Khóa DES",
                    DESModule.generate_key,
                    key_hint="Nhập key DES dạng HEX, đúng 16 ký tự.",
                    allow_generate=(action == "encrypt"),
                )
                step = 3

            elif step == 3:
                try:
                    if action == "encrypt":
                        plaintext = prompt("Nhập văn bản cần mã hóa: ")
                        ct = DESModule.encrypt(plaintext, key)
                        print_result_box("Ciphertext (HEX)", ct)
                        return show_result_actions(ct)
                    else:
                        ct = prompt("Nhập Ciphertext (HEX): ")
                        pt = DESModule.decrypt(ct, key)
                        print_result_box("Plaintext (kết quả giải mã)", pt)
                        return show_result_actions(pt)
                except (NavigateBack, NavigateMain, NavigateQuit):
                    raise
                except Exception as e:
                    print_error(str(e))
                    return "R"

        except NavigateBack:
            if step > 1:
                step -= 1
            else:
                return "B"

        except NavigateMain:
            return "M"

        except NavigateQuit:
            return "Q"


def _3des_flow() -> str:
    print_section("🔷 3DES (Triple DES)")
    print_info("Khóa: 16 hoặc 24 bytes (HEX) | Chế độ hỗ trợ: ECB")

    step = 1
    action = key = None

    while True:
        try:
            if step == 1:
                action = prompt_encrypt_or_decrypt()
                step = 2

            elif step == 2:
                key = _prompt_hex_key(
                    "Khóa 3DES",
                    TripleDESModule.generate_key,
                    key_hint="Nhập key 3DES dạng HEX: 32 ký tự (16 bytes) hoặc 48 ký tự (24 bytes).",
                    allow_generate=(action == "encrypt"),
                )
                step = 3

            elif step == 3:
                try:
                    if action == "encrypt":
                        plaintext = prompt("Nhập văn bản cần mã hóa: ")
                        ct = TripleDESModule.encrypt(plaintext, key)
                        print_result_box("Ciphertext (HEX)", ct)
                        return show_result_actions(ct)
                    else:
                        ct = prompt("Nhập Ciphertext (HEX): ")
                        pt = TripleDESModule.decrypt(ct, key)
                        print_result_box("Plaintext (kết quả giải mã)", pt)
                        return show_result_actions(pt)
                except (NavigateBack, NavigateMain, NavigateQuit):
                    raise
                except Exception as e:
                    print_error(str(e))
                    return "R"

        except NavigateBack:
            if step > 1:
                step -= 1
            else:
                return "B"

        except NavigateMain:
            return "M"

        except NavigateQuit:
            return "Q"


def symmetric_menu() -> str:
    """Menu mã hóa đối xứng. Trả về 'M'/'Q' khi người dùng thoát."""
    while True:
        try:
            print_section("🔐 Mã hóa Đối xứng (Symmetric Encryption)")
            algo_opts = {
                "1": "AES  — Advanced Encryption Standard (khuyến nghị)",
                "2": "DES  — Data Encryption Standard  ⚠ (không còn an toàn)",
                "3": "3DES — Triple DES",
            }
            choice = prompt_menu(algo_opts, "Chọn thuật toán",
                                 back_label="⬅  Quay về Menu chính")

        except NavigateBack:
            return "M"
        except NavigateMain:
            return "M"
        except NavigateQuit:
            return "Q"

        flow_map = {"1": _aes_flow, "2": _des_flow, "3": _3des_flow}

        while True:
            result = flow_map[choice]()
            if result == "R":
                continue
            elif result == "B":
                break
            elif result == "M":
                return "M"
            elif result == "Q":
                return "Q"
            else:
                break
