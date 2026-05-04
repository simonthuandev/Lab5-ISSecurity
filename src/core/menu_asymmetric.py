from core.input_handler import (
    prompt, prompt_menu,
    NavigateBack, NavigateMain, NavigateQuit,
)
from core.output_handler import (
    print_section, print_result_box, print_key_box,
    print_error, print_info, print_warning, show_result_actions,
)
from asymmetric.rsa_tool import generate_keys, encrypt_text, decrypt_text


_session_public_key: str | None = None
_session_private_key: str | None = None


def _generate_and_show_keys() -> tuple[str, str]:
    """Tạo và hiển thị cặp khóa RSA. Có nút [B] quay lại."""
    global _session_public_key, _session_private_key

    print_info("Đang tạo cặp khóa RSA-2048... (có thể mất vài giây)")
    pub, priv = generate_keys()
    _session_public_key = pub
    _session_private_key = priv

    print_key_box("PUBLIC KEY (dùng để mã hóa)", pub)
    print_key_box("PRIVATE KEY (dùng để giải mã — giữ bí mật!)", priv)
    print_warning("Lưu lại cặp khóa này! Chúng sẽ không được lưu sau khi thoát.")
    return pub, priv


def _get_or_input_key(label: str, session_key: str | None) -> str:
    """Dùng khóa từ phiên hoặc cho phép nhập thủ công. Có nút [B]."""
    if session_key:
        opts = {
            "1": f"Dùng {label} đã tạo trong phiên này",
            "2": f"Nhập {label} thủ công (PEM format)",
        }
        choice = prompt_menu(opts, f"Chọn nguồn {label}")
        if choice == "1":
            return session_key
    else:
        print_info(f"Chưa có {label} trong phiên này.")

    lines = []
    print_info(f"Dán {label} (PEM) vào đây, nhấn Enter 2 lần để kết thúc:")
    while True:
        line = input()
        if line == "" and lines and lines[-1] == "":
            break
        lines.append(line)
    return "\n".join(lines[:-1]).strip()


def _rsa_flow() -> str:
    global _session_public_key, _session_private_key

    print_section("🔑 RSA (Rivest–Shamir–Adleman)")
    print_info("Mã hóa bất đối xứng — Public Key mã hóa, Private Key giải mã")

    step = 1
    action = None

    while True:
        try:
            if step == 1:
                main_opts = {
                    "1": "Tạo cặp khóa mới (Public + Private Key)",
                    "2": "Mã hóa văn bản (dùng Public Key)",
                    "3": "Giải mã văn bản (dùng Private Key)",
                }
                action = prompt_menu(main_opts, "Chọn thao tác RSA",
                                     back_label="⬅  Quay về Menu chính")
                step = 2

            elif step == 2:
                if action == "1":
                    _generate_and_show_keys()
                    return show_result_actions(_session_public_key or "")

                elif action == "2":
                    pub_key = _get_or_input_key("Public Key", _session_public_key)
                    step = 3

                elif action == "3":
                    priv_key = _get_or_input_key("Private Key", _session_private_key)
                    step = 3

            elif step == 3:
                try:
                    if action == "2":
                        plaintext = prompt("Nhập văn bản cần mã hóa: ")
                        ct = encrypt_text(plaintext, pub_key)
                        print_result_box("Ciphertext (Base64)", ct)
                        return show_result_actions(ct)
                    else:
                        ct_input = prompt("Nhập Ciphertext (Base64): ")
                        pt = decrypt_text(ct_input, priv_key)
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


def asymmetric_menu() -> str:
    """Menu mã hóa bất đối xứng. Trả về 'M'/'Q'."""
    while True:
        result = _rsa_flow()
        if result in ("R", "B"):
            continue
        return result
