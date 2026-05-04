from core.input_handler import (
    prompt, prompt_menu,
    NavigateBack, NavigateMain, NavigateQuit,
)
from core.output_handler import (
    print_section, print_result_box,
    print_error, print_warning, print_info, show_result_actions,
)
from hash.md5 import MD5Tool
from hash.sha256 import sha256_hash


def _hash_flow(algo: str) -> str:
    if algo == "MD5":
        print_section("🔷 MD5 (Message Digest 5)")
        print_warning("MD5 không còn an toàn về mặt mật mã — chỉ dùng cho giáo dục!")
        hash_fn = MD5Tool.generate_hash
    else:
        print_section("🔷 SHA-256 (Secure Hash Algorithm 256-bit)")
        print_info("SHA-256 được khuyến nghị cho các ứng dụng hiện đại.")
        hash_fn = sha256_hash

    step = 1
    while True:
        try:
            if step == 1:
                text = prompt("Nhập văn bản cần băm (hoặc [B] quay lại): ")
                step = 2

            elif step == 2:
                try:
                    digest = hash_fn(text)
                    print_result_box(f"Hash {algo} (Hex Digest)", digest)
                    print_info(f"Độ dài digest: {len(digest) * 4} bits ({len(digest)} ký tự hex)")
                    return show_result_actions(digest)
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


def hash_menu() -> str:
    """Menu hàm băm. Trả về 'M'/'Q'."""
    while True:
        try:
            print_section("🔏 Hàm Băm (Hash Functions)")
            algo_opts = {
                "1": "SHA-256  — Secure Hash Algorithm 256-bit (khuyến nghị)",
                "2": "MD5     — Message Digest 5  ⚠ (không còn an toàn)",
            }
            choice = prompt_menu(algo_opts, "Chọn thuật toán băm",
                                 back_label="⬅  Quay về Menu chính")

        except NavigateBack:
            return "M"
        except NavigateMain:
            return "M"
        except NavigateQuit:
            return "Q"

        algo = "SHA-256" if choice == "1" else "MD5"

        while True:
            result = _hash_flow(algo)
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
