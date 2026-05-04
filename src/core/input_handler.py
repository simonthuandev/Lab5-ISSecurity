import base64
import sys
from core.output_handler import (
    BOLD, CYAN, RESET, DIM,
    print_warning, print_info,
)


# ── Navigation signals ────────────────────────────────────────────────────────

class NavigateBack(Exception):
    """Quay về menu / bước trước."""

class NavigateMain(Exception):
    """Về Menu chính."""

class NavigateQuit(Exception):
    """Thoát chương trình."""


# ── Helpers ───────────────────────────────────────────────────────────────────

def _handle_nav(choice: str):
    """Chuyển ký tự điều hướng thành exception tương ứng."""
    if choice == "B":
        raise NavigateBack
    if choice == "M":
        raise NavigateMain
    if choice == "Q":
        raise NavigateQuit


def prompt(message: str, allow_empty: bool = False) -> str:
    """Nhắc người dùng nhập chuỗi. Không cho phép chuỗi rỗng theo mặc định."""
    while True:
        try:
            value = input(f"{BOLD}{message}{RESET}").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            raise NavigateQuit
        if value or allow_empty:
            return value
        print_warning("Giá trị không được để trống. Vui lòng nhập lại.")


def prompt_menu(
    options: dict,
    title: str = "Chọn tùy chọn",
    back_label: str | None = "Quay lại bước trước",
    main_label: str | None = "Về Menu chính",
    quit_label: str | None = "Thoát chương trình",
) -> str:
    """
    Hiển thị menu có thêm tuỳ chọn điều hướng B / M / Q.
    Trả về key mà người dùng chọn (không bao gồm B/M/Q — những cái đó raise exception).

    Truyền back_label=None  để ẩn tuỳ chọn B.
    Truyền main_label=None  để ẩn tuỳ chọn M.
    Truyền quit_label=None  để ẩn tuỳ chọn Q.
    """
    display = dict(options)
    nav = {}
    if back_label:
        nav["B"] = back_label
    if main_label:
        nav["M"] = main_label
    if quit_label:
        nav["Q"] = quit_label

    print(f"\n{BOLD}{title}:{RESET}")
    for key, desc in display.items():
        print(f"  {CYAN}[{key}]{RESET} {desc}")

    if nav:
        print(f"{DIM}{'─' * 40}{RESET}")
        for key, desc in nav.items():
            print(f"  {CYAN}[{key}]{RESET} {desc}")

    print(f"{DIM}{'─' * 40}{RESET}")

    valid = set(k.upper() for k in {**display, **nav}.keys())

    while True:
        try:
            choice = input(f"{BOLD}Nhập lựa chọn: {RESET}").strip().upper()
        except (EOFError, KeyboardInterrupt):
            print()
            raise NavigateQuit

        if choice not in valid:
            print_warning(f"Lựa chọn không hợp lệ. Vui lòng chọn: {', '.join(sorted(valid))}")
            continue

        _handle_nav(choice)
        return choice


def prompt_mode(modes: list) -> str:
    """Chọn chế độ hoạt động (ECB / CBC)"""
    options = {str(i + 1): m for i, m in enumerate(modes)}
    key = prompt_menu(options, "Chọn chế độ hoạt động")
    return modes[int(key) - 1]


def prompt_key_or_generate(key_label: str, generator_fn, key_hint: str = "") -> bytes:
    """
    Hỏi người dùng muốn tự nhập khóa hay tự động tạo.
    Trả về khóa dạng bytes. Có nút [B] quay lại.
    """
    options = {
        "1": f"Tự nhập {key_label}",
        "2": f"Tự động tạo {key_label} ngẫu nhiên",
    }
    choice = prompt_menu(options, f"Quản lý {key_label}")

    if choice == "2":
        key = generator_fn()
        key_b64 = base64.b64encode(key).decode("utf-8")
        print_info(f"{key_label} (Base64): {key_b64}")
        return key

    # choice == "1": tự nhập
    if key_hint:
        print_info(key_hint)
    raw = prompt(f"Nhập {key_label}: ")
    try:
        decoded = base64.b64decode(raw)
        return decoded
    except Exception:
        return raw.encode("utf-8")


def prompt_encrypt_or_decrypt() -> str:
    """Hỏi người dùng muốn mã hóa hay giải mã. Có nút [B] quay lại."""
    options = {"1": "Mã hóa (Encrypt)", "2": "Giải mã (Decrypt)"}
    choice = prompt_menu(options, "Chọn thao tác")
    return "encrypt" if choice == "1" else "decrypt"
